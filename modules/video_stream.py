import os.path
from picamera2 import Picamera2
from libcamera import controls
import cv2
import time
import psutil
import logging
import threading
import queue
import numpy as np
from ultralytics import YOLO
from typing import Generator, Tuple, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStream:
    def __init__(self, target_fps: int = 30, jpeg_quality: int = 80, queue_size: int = 5):
        self.camera = None
        self.camera_type = None
        self.is_streaming = True
        self.is_ai_mode = False
        self.lock = threading.Lock()
        self.frame_queue = queue.Queue(maxsize=queue_size)
        self.yolo_model = self.init_ai()

        # Capture parameters
        self.target_fps = target_fps
        self.jpeg_quality = jpeg_quality

        # Metrics tracking
        self.frame_count = 0
        self.last_metrics_update = time.time()
        self.fps = 0

        self.stats = {
            'fps': 0,
            'resolution': '0x0',
            'quality': self.jpeg_quality,
            'bitrate': 0,
            'cpu_usage': 0
        }

        # Initialize the camera and start the capture thread
        self.init_camera()
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

    def init_camera(self):
        """Initialize camera with Pi Camera priority, fallback to USB."""
        # Try Pi Camera first
        try:
            logger.info("Attempting to initialize Pi Camera")
            self.camera = Picamera2()

            if not self.camera.sensor_modes:
                raise RuntimeError("No Pi Camera detected - check camera connection")

            config = self.camera.create_preview_configuration()
            self.camera.configure(config)
            self.camera.start()

            # Calculate µs/frame for target FPS and set controls
            frame_time = int(1_000_000 / self.target_fps)
            self.camera.set_controls({
                "AeEnable": True,
                "AwbEnable": True,
                "FrameDurationLimits": (frame_time, frame_time)
            })

            self.camera_type = 'picam'
            logger.info("Available sensor modes: %s", self.camera.sensor_modes)
            self.stats['resolution'] = f'{config["main"]["size"][0]}x{config["main"]["size"][1]}'
            return
        except Exception as e:
            logger.error("Pi Camera initialization failed: %s", str(e), exc_info=True)
            if self.camera and hasattr(self.camera, 'close'):
                self.camera.close()

        logger.warning("Falling back to USB camera")
        # Fallback to USB camera
        for device in [0, 1]:
            cap = cv2.VideoCapture(device)
            if cap.isOpened():
                self.camera = cap
                self.camera_type = 'usb'
                width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.stats['resolution'] = f'{width}x{height}'
                logger.info("Initialized USB Camera successfully on device %s", device)
                return

        raise RuntimeError("No camera available (tried Pi Camera and USB)")

    def init_ai(self):
        # Compiling to ncnn for ARM based chips like rpi5
        if not os.path.exists("./yolo11n_ncnn_model"):
            YOLO("yolo11n.pt").export(format="ncnn")
        return YOLO("./yolo11n_ncnn_model")

    def _capture_loop(self):
        """Continuously capture frames in a separate thread."""
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
        while True:
            while not self.is_streaming:
                continue
            frame = None
            try:
                if self.camera_type == 'usb':
                    success, frame = self.camera.read()
                    if not success or frame is None:
                        logger.error("Failed to read from USB camera")
                        continue
                    # Convert BGR to RGB for consistent color representation
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Optional: Flip the frame horizontally
                    frame = cv2.flip(frame, 1)
                else:  # picam
                    frame = self.camera.capture_array()
                    # Ensure frame is in RGB format
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                logger.error("Error capturing frame: %s", str(e))
                continue

            if frame is None:
                continue

            if self.is_ai_mode:
                # logger.info(self.yolo_model(frame)[0].plot())
                frame = self.yolo_model(frame)[0].plot()

            # JPEG encode the frame
            success, buffer = cv2.imencode('.jpg', frame, encode_params)
            if not success:
                logger.error("Failed to encode frame")
                continue
            frame_bytes = buffer.tobytes()

            # Update metrics
            self._update_metrics(len(frame_bytes))
            
            # Put frame in queue; if full, drop the frame
            try:
                self.frame_queue.put(frame_bytes, timeout=0.01)
            except queue.Full:
                logger.debug("Frame queue full; dropping frame")
                continue

            # Sleep to throttle capture rate based on target FPS
            time.sleep(1 / self.target_fps)

    def _update_metrics(self, frame_size: int):
        """Update streaming metrics less frequently (e.g., every second)."""
        with self.lock:
            self.frame_count += 1
            now = time.time()
            elapsed = now - self.last_metrics_update
            if elapsed >= 1.0:
                self.fps = self.frame_count / elapsed
                cpu_usage = psutil.cpu_percent(interval=None)
                # Bitrate: approximate kbps = (frame_size * fps * 8) / 1024
                bitrate = (frame_size * self.fps * 8) / 1024
                self.stats.update({
                    'fps': round(self.fps, 1),
                    'quality': self.jpeg_quality,
                    'bitrate': round(bitrate, 1),
                    'cpu_usage': round(cpu_usage, 1)
                })
                logger.info("Video Stats - FPS: %s, Quality: %s%%, Bitrate: %s kbps, CPU: %s%%",
                            self.stats['fps'], self.stats['quality'], self.stats['bitrate'], self.stats['cpu_usage'])
                # Reset metrics counters
                self.frame_count = 0
                self.last_metrics_update = now

    def generate_frames(self) -> Generator[bytes, None, None]:
        """Generate frames for streaming from the capture thread queue."""
        while self.is_streaming:
            try:
                frame_bytes = self.frame_queue.get(timeout=1)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except queue.Empty:
                continue

    def toggle_stream(self) -> bool:
        """Toggle streaming state."""
        self.is_streaming = not self.is_streaming
        logger.info("Streaming %s", "started" if self.is_streaming else "stopped")
        return self.is_streaming

    def toggle_ai(self) -> bool:
        """Toggle ai mode."""
        self.is_ai_mode = not self.is_ai_mode
        logger.info("AI Mode  %s", "started" if self.is_streaming else "stopped")
        return self.is_ai_mode


    def get_stats(self) -> Dict:
        """Get current streaming statistics."""
        with self.lock:
            return self.stats.copy()

    def __del__(self):
        if not (hasattr(self, "camera") and self.camera):
            return
        try:
            self.camera.release() if self.camera_type == "usb" else self.camera.close()
        except Exception:
            pass
        logger.info("Camera resources released")


# Create a singleton instance to be used across the application
video_stream = VideoStream()
