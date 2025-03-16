import cv2
from typing import Generator, Tuple, Optional

class VideoStream:
    def __init__(self):
        self.camera = None
        self.camera_type = None
        self.is_streaming = True
        self.init_camera()

    def init_camera(self):
        """Initialize camera with Pi Camera priority, fallback to USB."""
        # Try Pi Camera first
        try:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            self.camera.start()
            self.camera_type = 'picam'
            print("Initialized Pi Camera successfully")
            return
        except (ImportError, Exception) as e:
            print(f"Pi Camera initialization failed: {str(e)}, trying USB camera")
            pass

        # Fallback to USB camera
        for device in [0, 1]:
            self.camera = cv2.VideoCapture(device)
            if self.camera.isOpened():
                self.camera_type = 'usb'
                print("Initialized USB Camera successfully")
                return

        raise RuntimeError("No camera available (tried Pi Camera and USB)")

    def get_frame(self) -> Tuple[bool, Optional[bytes]]:
        """Capture and encode a single frame."""
        if not self.camera:
            return False, None
            
        try:
            if self.camera_type == 'usb':
                success, frame = self.camera.read()
                if not success:
                    return False, None
            else:  # picam
                frame = self.camera.capture_array()
            
            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            return True, buffer.tobytes()
        except Exception:
            return False, None

    def generate_frames(self) -> Generator[bytes, None, None]:
        """Generate frames for streaming."""
        while self.is_streaming:
            success, frame_bytes = self.get_frame()
            if not success:
                break
            
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def toggle_stream(self) -> bool:
        """Toggle streaming state."""
        self.is_streaming = not self.is_streaming
        return self.is_streaming

    def __del__(self):
        """Release camera resources."""
        if self.camera:
            if self.camera_type == 'usb':
                self.camera.release()
            else:  # picam
                self.camera.close()

# Create a single instance to be used across the application
video_stream = VideoStream()
