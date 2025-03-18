# 🤖 Robot Control Dashboard

A modern web interface for controlling and monitoring your Raspberry Pi-powered robot with real-time video streaming, system monitoring, and sensor data visualization.

## ✨ Features

- 📹 **Live Video Streaming**: Real-time camera feed with controls
  - Automatic camera detection (Pi Camera Module and USB cameras)
  - Quality/resolution controls
  - Stream performance optimization
  - Error handling with fallback display
  - Video recording capability

- 📊 **System Monitoring**: 
  - CPU usage and temperature tracking
  - Memory usage monitoring
  - Real-time performance metrics
  - Historical data visualization

- 🎮 **Robot Controls**:
  - Directional movement interface
  - Arm/gripper control panel
  - Path visualization
  - Emergency stop functionality

- 📡 **Sensor Integration**:
  - Real-time sensor data display
  - Ultrasonic distance readings
  - LIDAR measurements
  - Custom sensor support

- 📈 **Performance Charts**:
  - Real-time data plotting
  - System resource monitoring
  - Temperature tracking

## 🚀 Quick Set-Up for the first time

1. **Setup Environment**
   ```bash
   python3 -m venv --system-site-packages venv 
   source venv/bin/activate
   ```

2. **Install Dependencies**

   First, install required system packages:
   ```bash
   # Install necessary Pi Camera packages for Raspberry Pi camera support
   sudo apt update && sudo apt install -y libcamera-dev python3-libcamera python3-picamera2
   ```

   Then install Python packages: (Run this again if you installed new packages)
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
   Note: `--no-cache-dir`: Prevents caching of downloaded packages to save space on low-memory systems like Raspberry Pi.

### Optional: Test Pi Camera Functionality

1. **Still Capture**
   - File: `camera_tests/still_capture.py`
   - Usage: Captures a single photo saved in `camera_tests/test_files/`
    ```bash
    python3 camera_tests/still_capture.py
    ```

2. **Video Capture**
   - File: `camera_tests/video_capture.py`
   - Usage: Records a video saved in `camera_tests/test_files/`
   ```bash
   python3 camera_tests/video_capture.py
    ```

3. **Configuration Test**
   - File: `camera_tests/configuration_test.py`
   - Usage: Tests different camera configurations
   ```bash
   python3 camera_tests/configuration_test.py
    ```

3. **Start Server**
   ```bash
   python app.py
   ```

4. **Access Dashboard**
   - Open `http://<raspberry_pi_ip>:5000`
   - Default port: 5000

## On-going Development

### Development Mode
```bash
  # Start with hot-reload
  python app.py
```

### Restarting the Server after changes
```bash
  # Stop the server
  CTRL+C

  # Start the server again
  python app.py
```

## 🐳 Docker (Optional)

### Prerequisites
- Install Docker Engine:
  - [Raspberry Pi](https://docs.docker.com/engine/install/raspberry-pi-os/)
  - [macOS](https://docs.docker.com/desktop/install/mac-install/)
  - [Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Linux](https://docs.docker.com/engine/install/)

### Quick Run
```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Development Mode
```bash
# Start with hot-reload
docker compose -f docker-compose.dev.yml up

# Rebuild on dependency changes
docker compose -f docker-compose.dev.yml build --no-cache
```

### Platform-Specific Notes

#### Raspberry Pi
```bash
# Build with resource limits
docker compose up -d --build

# Monitor resources
docker stats robot-dashboard
```

### Useful Commands

#### Container Management
```bash
# Start container
docker compose start

# Stop container
docker compose stop

# Restart container
docker compose restart

# Remove container
docker compose down
```

#### Development
```bash
# View logs with timestamps
docker compose logs -f --timestamps

# Shell access
docker compose exec web bash

# Check container health
docker compose ps
```

#### Troubleshooting
```bash
# View resource usage
docker stats

# Check logs for errors
docker compose logs -f --tail=100

# Rebuild from scratch
docker compose build --no-cache
```

## 🔧 Requirements

- Raspberry Pi (3/4/Zero 2W)
- Python 3.7+
- USB Camera or Pi Camera Module
  - For Pi Camera: requires python3-picamera2 package (install via apt)
  - For USB Camera: automatically supported via OpenCV
- Internet connection for initial setup

## 📦 Key Dependencies

- Flask 3.0.0: Web framework
- OpenCV 4.8.1: Video processing
- picamera2: Raspberry Pi camera interface (system package)
- psutil 5.9.5: System monitoring
- NumPy 1.24.3: Data processing
- Werkzeug 3.0.1: WSGI utilities
- gunicorn 21.2.0: WSGI HTTP Server
- Flask-Cors 4.0.0: Cross-origin support

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- How to submit issues
- How to submit pull requests
- Development workflow
- Code standards

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Flask community
- OpenCV contributors
- Raspberry Pi Foundation
