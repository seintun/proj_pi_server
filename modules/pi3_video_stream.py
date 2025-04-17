import cv2
import time
import psutil
import logging
import threading
import queue
import numpy as np
from typing import Generator, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStream:
    def __init__(self, target_fps: int = 30, jpeg_quality: int = 80, queue_size: int = 5):
        self.camera = None
        self.camera_type = None
        self.is_streaming = True
        self.lock = threading.Lock()
        self.frame_queue = queue.Queue(maxsize=queue_size)

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
        """Initialize camera with PiCamera priority, fallback to USB."""
        try:
            from picamera import PiCamera
            from picamera.array import PiRGBArray

            logger.info("Attempting to initialize Pi Camera")
            self.camera = PiCamera()
            self.camera.resolution = (1280, 720)  # Set default resolution
            self.camera.framerate = self.target_fps

            self.raw_capture = PiRGBArray(self.camera, size=self.camera.resolution)
            self.camera_type = 'picam'
            logger.info("Pi Camera initialized successfully")

            self.stats['resolution'] = f"{self.camera.resolution[0]}x{self.camera.resolution[1]}"
            return
        except Exception as e:
            logger.error("Pi Camera initialization failed: %s", str(e), exc_info=True)

        # Fallback to USB camera
        logger.warning("Falling back to USB camera")
        for device in [0, 1]:
            cap = cv2.VideoCapture(device)
            if cap.isOpened():
                self.camera = cap
                self.camera_type = 'usb'
                width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.stats['resolution'] = f"{width}x{height}"
                logger.info("Initialized USB Camera successfully on device %s", device)
                return

        raise RuntimeError("No camera available (tried Pi Camera and USB)")

    def _capture_loop(self):
        """Continuously capture frames in a separate thread."""
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
        
        if self.camera_type == "picam":
            from picamera.array import PiRGBArray
            stream = self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True)
        
        while self.is_streaming:
            frame = None
            try:
                if self.camera_type == "usb":
                    success, frame = self.camera.read()
                    if not success or frame is None:
                        logger.error("Failed to read from USB camera")
                        continue
                    frame = cv2.flip(frame, 1)  # Optional: Flip horizontally
                else:  # picam
                    raw_frame = next(stream)
                    frame = raw_frame.array
                    self.raw_capture.truncate(0)  # Clear buffer for next frame

            except Exception as e:
                logger.error("Error capturing frame: %s", str(e))
                continue

            if frame is None:
                continue

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

            # Sleep to match target FPS
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
                bitrate = (frame_size * self.fps * 8) / 1024  # Approximate kbps
                self.stats.update({
                    'fps': round(self.fps, 1),
                    'quality': self.jpeg_quality,
                    'bitrate': round(bitrate, 1),
                    'cpu_usage': round(cpu_usage, 1)
                })
                logger.info("Video Stats - FPS: %s, Quality: %s%%, Bitrate: %s kbps, CPU: %s%%",
                            self.stats['fps'], self.stats['quality'], self.stats['bitrate'], self.stats['cpu_usage'])
                # Reset counters
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

    def get_stats(self) -> Dict:
        """Get current streaming statistics."""
        with self.lock:
            return self.stats.copy()

    def __del__(self):
        """Release camera resources on exit."""
        if hasattr(self, "camera") and self.camera:
            try:
                if self.camera_type == "usb":
                    self.camera.release()
                else:
                    self.camera.close()
            except Exception:
                pass
            logger.info("Camera resources released")


# Create a singleton instance to be used across the application
video_stream = VideoStream()
