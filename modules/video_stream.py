import cv2
import time
import psutil
from typing import Generator, Tuple, Optional, Dict
from threading import Lock
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStream:
    def __init__(self):
        self.camera = None
        self.camera_type = None
        self.is_streaming = True
        self.lock = Lock()
        
        # Metrics tracking
        self.frame_count = 0
        self.last_frame_time = time.time()
        self.frame_times = []  # Track last 30 frame times for FPS calculation
        self.max_frame_times = 30
        self.current_resolution = (0, 0)
        self.current_quality = 100
        self.last_frame_size = 0
        self.bitrate_window = []  # Track last 10 frame sizes for bitrate calculation
        self.max_bitrate_samples = 10
        
        self.stats = {
            'fps': 0,
            'resolution': '0x0',
            'quality': 100,
            'bitrate': 0,
            'cpu_usage': 0
        }
        
        self.init_camera()

    def init_camera(self):
        """Initialize camera with Pi Camera priority, fallback to USB."""
        # Try Pi Camera first
        try:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            self.camera.start()
            self.camera_type = 'picam'
            logger.info("Initialized Pi Camera successfully")
            
            # Get resolution from Pi Camera
            config = self.camera.camera_config
            self.current_resolution = (config["main"]["size"][0], config["main"]["size"][1])
            return
        except (ImportError, Exception) as e:
            logger.warning(f"Pi Camera initialization failed: {str(e)}, trying USB camera")
            pass

        # Fallback to USB camera
        for device in [0, 1]:
            self.camera = cv2.VideoCapture(device)
            if self.camera.isOpened():
                self.camera_type = 'usb'
                
                # Get resolution from USB camera
                width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.current_resolution = (width, height)
                
                logger.info("Initialized USB Camera successfully")
                return

        raise RuntimeError("No camera available (tried Pi Camera and USB)")

    def update_metrics(self, frame_bytes: bytes):
        """Update streaming metrics."""
        current_time = time.time()
        
        with self.lock:
            # Update frame count and timing
            self.frame_count += 1
            
            # Calculate FPS
            frame_time = current_time - self.last_frame_time
            self.frame_times.append(frame_time)
            if len(self.frame_times) > self.max_frame_times:
                self.frame_times.pop(0)
            avg_frame_time = np.mean(self.frame_times)
            current_fps = 1 / avg_frame_time if avg_frame_time > 0 else 0
            
            # Calculate bitrate
            frame_size = len(frame_bytes)
            self.bitrate_window.append(frame_size)
            if len(self.bitrate_window) > self.max_bitrate_samples:
                self.bitrate_window.pop(0)
            avg_frame_size = np.mean(self.bitrate_window)
            bitrate = (avg_frame_size * current_fps * 8) / 1024  # kbps
            
            # Get CPU usage
            cpu_usage = psutil.cpu_percent()
            
            # Update stats
            self.stats.update({
                'fps': round(current_fps, 1),
                'resolution': f'{self.current_resolution[0]}x{self.current_resolution[1]}',
                'quality': self.current_quality,
                'bitrate': round(bitrate, 1),
                'cpu_usage': round(cpu_usage, 1)
            })
            
            # Log stats periodically (every 30 frames)
            if self.frame_count % 30 == 0:
                logger.info(f"Video Stats - FPS: {current_fps:.1f}, Quality: {self.current_quality}%, "
                          f"Bitrate: {bitrate:.1f} kbps, CPU: {cpu_usage:.1f}%")
            
            self.last_frame_time = current_time
            self.last_frame_size = frame_size

    def get_frame(self) -> Tuple[bool, Optional[bytes]]:
        """Capture and encode a single frame."""
        if not self.camera or not self.is_streaming:
            return False, None
            
        try:
            if self.camera_type == 'usb':
                success, frame = self.camera.read()
                if not success:
                    logger.error("Failed to read from USB camera")
                    return False, None
                # Flip horizontal for USB camera
                frame = cv2.flip(frame, 1)
            else:  # picam
                try:
                    frame = self.camera.capture_array()
                except Exception as e:
                    logger.error(f"Failed to capture from Pi Camera: {str(e)}")
                    return False, None
            
            # Convert frame to JPEG format at current quality
            encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), self.current_quality]
            _, buffer = cv2.imencode('.jpg', frame, encode_params)
            frame_bytes = buffer.tobytes()
            
            # Update metrics
            self.update_metrics(frame_bytes)
            
            return True, frame_bytes
        except Exception as e:
            logger.error(f"Error capturing frame: {str(e)}")
            return False, None

    def generate_frames(self) -> Generator[bytes, None, None]:
        """Generate frames for streaming."""
        try:
            while self.is_streaming:
                success, frame_bytes = self.get_frame()
                if not success:
                    logger.warning("No frame available, stopping stream")
                    break
                
                yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            logger.error(f"Error in generate_frames: {str(e)}")

    def toggle_stream(self) -> bool:
        """Toggle streaming state."""
        self.is_streaming = not self.is_streaming
        logger.info(f"Streaming {'started' if self.is_streaming else 'stopped'}")
        return self.is_streaming

    def get_stats(self) -> Dict:
        """Get current streaming statistics."""
        with self.lock:
            return self.stats.copy()

    def __del__(self):
        """Release camera resources."""
        if self.camera:
            if self.camera_type == 'usb':
                self.camera.release()
            else:  # picam
                self.camera.close()
            logger.info("Camera resources released")

# Create a single instance to be used across the application
video_stream = VideoStream()
