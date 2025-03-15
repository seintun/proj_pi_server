import cv2
from typing import Generator, Tuple, Optional

class VideoStream:
    def __init__(self):
        # Try both USB and Pi Camera devices
        self.camera = None
        for device in [0, 1]:
            self.camera = cv2.VideoCapture(device)
            if self.camera.isOpened():
                break
        if not self.camera or not self.camera.isOpened():
            raise RuntimeError("Could not open video device")
        self.is_streaming = True

    def get_frame(self) -> Tuple[bool, Optional[bytes]]:
        """Capture and encode a single frame."""
        success, frame = self.camera.read()
        if not success:
            return False, None
        
        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        return True, buffer.tobytes()

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
        self.camera.release()

# Create a single instance to be used across the application
video_stream = VideoStream()
