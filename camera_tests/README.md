# Camera Tests

This directory contains test scripts for the Pi Camera setup.

## Available Tests

1. **Still Capture**
   - File: `still_capture.py`
   - Usage: Captures a single photo saved in `test_files/`
   - Run: `python3 still_capture.py`

2. **Video Capture**
   - File: `video_capture.py`
   - Usage: Records a video saved in `test_files/`
   - Run: `python3 video_capture.py`

3. **Configuration Test**
   - File: `configuration_test.py`
   - Usage: Tests different camera configurations
   - Run: `python3 configuration_test.py`

## Requirements
- Raspberry Pi OS (Bullseye or later)
- Python 3.7+
- Pi Camera module connected
- libcamera and Picamera2 installed

## Installation
```bash
sudo apt update
sudo apt install libcamera-dev python3-libcamera
pip install picamera2
```

## Troubleshooting
- Ensure camera is enabled in raspi-config
- Check camera connection
- Verify libcamera installation
