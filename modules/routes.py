from flask import Blueprint, render_template, Response, jsonify
from .video_stream import video_stream
from .sensor_interface import sensor_interface
from .object_detection.detector import object_detector

# Create blueprint for all routes
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    """Serve the HTML page with video stream and buttons."""
    return render_template('index.html')

@routes.route('/video_feed')
def video_feed():
    """Route for streaming the video feed."""
    return Response(
        video_stream.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@routes.route('/toggle_stream', methods=['POST'])
def toggle_stream():
    """Toggle video streaming on/off."""
    is_streaming = video_stream.toggle_stream()
    return jsonify({"streaming": is_streaming})

@routes.route('/action', methods=['GET'])
def action():
    """Custom Raspberry Pi action."""
    print("Button clicked! Performing Raspberry Pi action...")
    # Example: Run a script, turn on LED, etc.
    return jsonify({"message": "Action executed on Raspberry Pi!"})

# New routes for sensor data and object detection
@routes.route('/sensor/start', methods=['POST'])
def start_sensor():
    """Start sensor data collection."""
    sensor_interface.start_collection()
    return jsonify({"status": "Sensor collection started"})

@routes.route('/sensor/stop', methods=['POST'])
def stop_sensor():
    """Stop sensor data collection."""
    sensor_interface.stop_collection()
    return jsonify({"status": "Sensor collection stopped"})

@routes.route('/sensor/data', methods=['GET'])
def get_sensor_data():
    """Get latest sensor data."""
    data = sensor_interface.get_latest_data()
    return jsonify(data)

@routes.route('/sensor/batch', methods=['GET'])
def get_sensor_batch():
    """Get batch of sensor readings."""
    batch = sensor_interface.get_data_batch()
    return jsonify({"data": batch})

@routes.route('/detection/status', methods=['GET'])
def get_detection_status():
    """Get object detection status."""
    return jsonify({
        "initialized": object_detector.is_initialized,
        "classes": object_detector.classes
    })

# Error handlers
@routes.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@routes.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
