# Contributing to Raspberry Pi Server Project

## Project Architecture

This document outlines the architecture, design patterns, and guidelines for contributing to the Raspberry Pi Server project.

### Directory Structure

```
proj_pi_server/
├── static/                 # Static assets
│   ├── css/               # Stylesheet files
│   │   └── styles.css     # Main stylesheet
│   ├── js/                # JavaScript files
│   │   └── app.js         # Main frontend logic
│   └── images/            # Image assets
├── templates/             # HTML templates
│   └── index.html         # Main page template
├── modules/               # Python module directory
│   ├── __init__.py
│   ├── routes.py         # Flask routes
│   ├── video_stream.py   # Video streaming functionality
│   ├── sensor_interface.py # Sensor data collection
│   └── object_detection/  # Object detection package
│       ├── __init__.py
│       └── detector.py    # YOLO model integration
├── app.py                # Application entry point
├── requirements.txt      # Python dependencies
└── Dockerfile           # Container configuration
```

## Module Responsibilities

### 1. Video Stream Module (`video_stream.py`)
- Handles camera initialization and management
- Provides frame capture functionality
- Manages streaming state
- Implements frame generation for Flask streaming

```python
# Example: Adding a new video processing feature
class VideoStream:
    def apply_filter(self, frame):
        # Add your filter logic here
        return processed_frame
```

### 2. Sensor Interface (`sensor_interface.py`)
- Manages sensor data collection
- Implements threading for concurrent data collection
- Provides data queuing and batch processing
- Handles sensor resource management

```python
# Example: Adding a new sensor type
class SensorInterface:
    def _read_new_sensor(self):
        # Implement new sensor reading logic
        return sensor_data
```

### 3. Object Detection (`object_detection/`)
- YOLO model integration
- Frame preprocessing
- Object detection and annotation
- Model management and configuration

```python
# Example: Adding a new detection model
class ObjectDetector:
    def load_custom_model(self, model_path):
        # Implement custom model loading
        pass
```

### 4. Routes (`routes.py`)
- HTTP endpoint definitions
- Request handling
- Response formatting
- Error handling

```python
# Example: Adding a new endpoint
@routes.route('/api/new-feature', methods=['POST'])
def new_feature():
    # Implement new feature logic
    return jsonify({"status": "success"})
```

## Adding New Features

### 1. Frontend Changes
1. Add new styles to `static/css/styles.css`
2. Add new JavaScript functions to `static/js/app.js`
3. Update `templates/index.html` with new UI elements

```javascript
// Example: Adding new frontend functionality
async function newFeature() {
    try {
        const response = await fetch('/api/new-feature');
        const data = await response.json();
        // Handle response
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### 2. Backend Changes
1. Create new module or extend existing ones in `modules/`
2. Add new routes in `routes.py`
3. Update requirements if needed
4. Document new functionality

```python
# Example: Creating a new module
# modules/new_feature.py
class NewFeature:
    def __init__(self):
        self.config = {}

    def process(self, data):
        # Implement processing logic
        return result
```

## Error Handling

1. Use appropriate HTTP status codes
2. Implement proper logging
3. Provide meaningful error messages
4. Handle both client and server errors

```python
@routes.errorhandler(CustomError)
def handle_custom_error(error):
    return jsonify({
        "error": str(error),
        "code": error.code
    }), error.status_code
```
