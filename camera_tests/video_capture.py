from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import time
from datetime import datetime
import os

def preview_video(duration: int = 5):
    """Record a short MP4 video using Picamera2, ensuring directory exists."""
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    # Generate a timestamped filename for output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"camera_tests/test_files/test_video_{timestamp}.mp4"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Create encoder and output objects
    encoder = H264Encoder(bitrate=4_000_000)  # 4 Mbps encoding bitrate
    output = FfmpegOutput(output_file, audio=False)  # Save to MP4 without audio

    # Start camera preview and recording
    picam2.start_preview()
    picam2.start_recording(encoder, output)
    print(f"Recording video for {duration} seconds to '{output_file}'...")

    time.sleep(duration)

    picam2.stop_recording()
    picam2.stop_preview()
    print(f"Recording complete. Video saved to '{output_file}'")


if __name__ == "__main__":
    preview_video()