# Contributing to Robot Control Dashboard

Welcome to the Robot Control Dashboard project! This guide will help you get started as a contributor, whether you're a developer or not.

## 🌟 For Everyone

### What This Project Does
The Robot Control Dashboard is a web interface for Raspberry Pi that provides:
- Live video streaming from a camera
- Real-time system monitoring (CPU, Memory, Temperature)
- Robot control interface
- Sensor data visualization

### Reporting Issues
1. Check if the issue already exists in the Issues tab
2. Use the issue template to provide:
   - What happened
   - What you expected to happen
   - Steps to reproduce
   - Screenshots (if applicable)

### Dashboard Features
- **Video Feed**: Live camera stream with start/stop control
- **System Stats**: Real-time monitoring of:
  - CPU usage and temperature
  - Memory usage
  - System sensors
- **Control Panel**: Robot movement and arm control
- **Charts**: Visual representation of system metrics

## 💻 For Developers

### Quick Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # Local install
# pip install --no-cache-dir -r requirements.txt 
# Use --no-cache-dir to save space on low-memory systems like Raspberry Pi
python app.py
```

### Project Structure
```
proj_pi_server/
├── app.py                   # Application entry point, Flask server setup
├── requirements.txt         # Python dependencies
├── modules/                 # Core backend functionality
│   ├── monitor/             # System monitoring modules
│   │   ├── cpu.py           # CPU metrics collection
│   │   ├── memory.py        # Memory usage tracking
│   │   ├── temperature.py   # Temperature monitoring
│   │   └── system_info.py   # System information aggregation
│   ├── routes.py            # API endpoints and route handlers
│   ├── sensor_interface.py  # Sensor data collection
│   ├── video_stream.py      # Video streaming implementation
│   └── object_detection/    # ML-based object detection
│       ├── detector.py      # Object detection logic
│       └── __init__.py     
├── static/                  # Frontend assets
│   ├── css/                 # Stylesheets
│   │   ├── dashboard.css    # Main dashboard styles
│   │   └── styles.css       # Common styles
│   ├── js/                  # JavaScript files
│   │   ├── app.js           # Main application logic
│   │   ├── dashboard.js     # Dashboard functionality
│   │   └── video-control.js # Video controls
│   └── img/                 # Image assets
└── templates/               # HTML templates
    ├── index.html           # Main application template
    └── dashboard.html       # Dashboard interface

```

### Key Components

1. **Monitor Module** (`modules/monitor/`)
   - `cpu.py`: Handles CPU metrics collection using psutil
   - `memory.py`: Manages memory usage monitoring
   - `temperature.py`: Tracks system temperature
   - `system_info.py`: Aggregates system metrics

2. **Video Stream** (`modules/video_stream.py`)
   - Manages camera initialization
   - Handles frame capture and processing
   - Implements streaming optimization
   - Provides error handling and fallback

3. **Sensor Interface** (`modules/sensor_interface.py`)
   - Manages sensor connections
   - Processes sensor data
   - Handles data conversion and calibration
   - Provides real-time readings

4. **Object Detection** (`modules/object_detection/`)
   - Implements ML-based detection
   - Processes video frames
   - Identifies objects in real-time
   - Provides detection coordinates

5. **Frontend Components**
   - **Dashboard** (`templates/dashboard.html`):
     - Main control interface
     - System metrics display
     - Video feed integration
     - Robot control panel
   - **JavaScript** (`static/js/`):
     - `dashboard.js`: Real-time updates and charts
     - `video-control.js`: Video stream management
     - `app.js`: Core application logic
   - **Stylesheets** (`static/css/`):
     - `dashboard.css`: Dashboard-specific styles
     - `styles.css`: Common styling elements

### Development Workflow

1. **Fork & Clone**
   - Fork the repository
   - Clone your fork locally
   - Set up development environment

2. **Branch**
   - Create feature branch: `feature/your-feature`
   - Create fix branch: `fix/issue-description`

3. **Develop**
   - Follow code style (PEP 8 for Python)
   - Add tests for new features
   - Keep changes focused and minimal

4. **Test**
   - Run existing tests
   - Test on Raspberry Pi if possible
   - Verify browser compatibility

5. **Submit**
   - Push to your fork
   - Create Pull Request
   - Respond to review comments

### Code Standards

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features
- **CSS**: Follow BEM naming
- **Commit Messages**: Clear and descriptive

### Testing Requirements

1. **Backend Tests**
   - Unit tests for new modules
   - Integration tests for API endpoints

2. **Frontend Tests**
   - Browser compatibility
   - Mobile responsiveness
   - Performance testing

## 🔧 Troubleshooting

Common issues and solutions:

1. **Video Stream Issues**
   - Check camera connection
   - Verify camera permissions
   - Check system logs

2. **System Monitor Issues**
   - Verify psutil installation
   - Check system permissions
   - Review error logs

3. **Frontend Issues**
   - Clear browser cache
   - Check console errors

Need more help? Join our community discussion or reach out to maintainers.
