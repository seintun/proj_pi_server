from picamera import PiCamera
import time
from datetime import datetime
import os
import subprocess

def preview_video(duration: int = 5):
    """Record a short video on Raspberry Pi 3 using picamera."""
    camera = PiCamera()

    # Set resolution and frame rate
    camera.resolution = (1280, 720)  # 720p HD recording
    camera.framerate = 30

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    h264_file = f"camera_tests/test_files/test_video_{timestamp}.h264"
    mp4_file = f"camera_tests/test_files/test_video_{timestamp}.mp4"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(h264_file), exist_ok=True)

    # Start preview (optional, can be removed)
    camera.start_preview()

    # Start recording in H.264 format
    print(f"Recording video for {duration} seconds to '{h264_file}'...")
    camera.start_recording(h264_file)

    time.sleep(duration)

    camera.stop_recording()
    camera.stop_preview()
    camera.close()
    print(f"Recording complete. Video saved as '{h264_file}'")

    # Convert H.264 to MP4 using FFmpeg
    print(f"Converting '{h264_file}' to MP4 format...")
    ffmpeg_cmd = [
        "ffmpeg", "-framerate", "30", "-i", h264_file, 
        "-c:v", "copy", "-y", mp4_file
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Conversion complete. MP4 saved as '{mp4_file}'")

if __name__ == "__main__":
    preview_video()
