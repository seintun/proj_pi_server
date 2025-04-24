from picamera2 import Picamera2
import os

def capture_photo(filename="camera_tests/test_files/test_still_image.jpg"):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    picam2 = Picamera2()
    picam2.start_and_capture_file(filename)
    print(f"Photo saved as {filename}")

if __name__ == "__main__":
    capture_photo()