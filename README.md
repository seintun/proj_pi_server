# 🤖 Robot Control Dashboard

A modern web interface for controlling and monitoring your Raspberry Pi-powered robot with real-time video streaming, system monitoring, and sensor data visualization.

## ✨ Features

- 📹 **Live Video Streaming**: Real-time camera feed with controls
  - Automatic camera detection
  - Quality/resolution controls
  - Stream performance optimization
  - Error handling with fallback display

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

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
    Note: `--no-cache-dir`: Prevents caching of downloaded packages to save space on low-memory systems like Raspberry Pi.

3. **Start Server**
   ```bash
   python app.py
   ```

4. **Access Dashboard**
   - Open `http://<raspberry_pi_ip>:5000`
   - Default port: 5000

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
- USB Camera or Pi Camera
- Internet connection for initial setup

## 📦 Key Dependencies

- Flask 3.0.0: Web framework
- OpenCV 4.8.1: Video processing
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
