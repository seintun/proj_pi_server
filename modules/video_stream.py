# Standard library imports
import io
import logging
import queue
import threading
import time
from typing import Generator, Dict

# Third-party imports
import psutil
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStream:
    def __init__(self, target_fps: int = 30, jpeg_quality: int = 80, queue_size: int = 5):
        self.camera = None
        self.is_streaming = True
        self.lock = threading.Lock()
        self.frame_queue = queue.Queue(maxsize=queue_size)
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
        """Initialize Pi Camera."""
        from picamera2 import Picamera2
        from libcamera import controls

        logger.info("Attempting to initialize Pi Camera")
        self.camera = Picamera2()

        if not self.camera.sensor_modes:
            raise RuntimeError("No Pi Camera detected - check camera connection")

        config = self.camera.create_preview_configuration()
        self.camera.configure(config)
        self.camera.start()

        # Set resolution in stats
        width = config["main"]["size"][0]
        height = config["main"]["size"][1]
        self.stats['resolution'] = f'{width}x{height}'

        # Calculate µs/frame for target FPS and set controls
        frame_time = int(1_000_000 / self.target_fps)
        self.camera.set_controls({
            "AeEnable": True,
            "AwbEnable": True,
            "FrameDurationLimits": (frame_time, frame_time)
        })

        logger.info("Pi Camera initialized successfully with configuration: %s", config)

    def _capture_loop(self):
        """Continuously capture frames in a separate thread."""
        while self.is_streaming:
            try:
                frame = self.camera.capture_array()
                
                # Convert RGBA frame to RGB, flip horizontally, and encode as JPEG
                img = Image.fromarray(frame).convert('RGB')
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
                with io.BytesIO() as output:
                    img.save(output, format="JPEG", quality=self.jpeg_quality)
                    frame_bytes = output.getvalue()
                
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
            except Exception as e:
                logger.error("Error capturing frame: %s", str(e))
                continue

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

    def get_stats(self) -> Dict:
        """Get current streaming statistics."""
        with self.lock:
            stats = self.stats.copy()
            stats['display_name'] = 'Pi-Cam'
            return {
                'status': 'success',
                'stats': stats
            }

    def __del__(self):
        if hasattr(self, "camera") and self.camera:
            try:
                self.camera.close()
            except Exception:
                pass
            logger.info("Camera resources released")


# Create a singleton instance to be used across the application
video_stream = VideoStream()
