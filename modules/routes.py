from flask import Blueprint, render_template, Response, send_file, jsonify, request
import json
import time
import os
import logging
from .monitor import SystemMonitor
from .video_stream import video_stream  # Import the singleton instance
from .gpio import gpio_controller
from .sensor_interface import sensor_interface

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)
system_monitor = SystemMonitor()

@routes.route('/')
def index():
    """Render the dashboard page"""
    return render_template('dashboard.html')

@routes.route('/system-events')
def system_events():
    """Server-Sent Events endpoint for system monitoring"""
    def generate():
        while True:
            # Get current stats
            stats = system_monitor.get_minimal_stats()
            if stats:
                yield f"data: {json.dumps(stats)}\n\n"
            time.sleep(1)  # Update every second
    
    return Response(generate(), mimetype='text/event-stream')

@routes.route('/api/system-stats')
def get_system_stats():
    """Get full system statistics including history"""
    return json.dumps(system_monitor.get_stats())

@routes.route('/video_feed')
def video_feed():
    """Video streaming route with error handling"""
    global video_stream
    
    try:
        if not video_stream:
            video_stream = VideoStream()
        
        return Response(
            video_stream.generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        # Log the error
        print(f"Error in video feed: {e}")
        # Return no-camera image
        return send_file('static/img/no-camera.png', mimetype='image/png')

@routes.route('/video/stats')
def get_video_stats():
    """Get video streaming statistics"""
    try:
        if not video_stream:
            raise RuntimeError("Video stream not initialized")
            
        stats = video_stream.get_stats()
        display_name = 'Pi-Cam' if video_stream.camera_type == 'picam' else 'Webcam' if video_stream.camera_type == 'usb' else 'No Camera'
        
        # If stream is not active, override some stats
        if not video_stream.is_streaming:
            stats.update({
                'fps': 0,
                'bitrate': 0,
                'cpu_usage': 0
            })
        
        return jsonify({
            'status': 'success',
            'stats': {
                **stats,
                'display_name': display_name
            }
        })
    except Exception as e:
        logger.error(f"Error getting video stats: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 503
        
@routes.route('/api/gpio/led/toggle', methods=['POST'])
def toggle_led():
    """Toggle LED state"""
    try:
        new_state = gpio_controller.toggle_led()
        return jsonify({
            'status': 'success',
            'state': new_state
        })
    except Exception as e:
        logger.error(f"Error toggling LED: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 503

@routes.route('/video/camera-type')
def get_camera_type():
    """Get current camera type"""
    try:
        return jsonify({
            'status': 'success',
            'type': video_stream.camera_type or 'none',
            'display_name': 'Pi-Cam' if video_stream.camera_type == 'picam' else 'Webcam' if video_stream.camera_type == 'usb' else 'No Camera'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 503

@routes.route('/ai/toggle', methods=['POST'])
def toggle_ai():
    """Toggle ai on/off"""
    successful = True
    message = "AI Mode Toggled Successfully"
    try:
        is_ai_mode  = video_stream.toggle_ai()
    except Exception as e:
        successful = False
        message = e
    return jsonify({
        'status': 'success' if successful else 'error',
        'streaming': is_ai_mode if successful else False,
        'message': message
    })

@routes.route('/video/toggle', methods=['POST'])
def toggle_video():
    """Toggle video stream on/off"""
    successful = True
    message = "Video stream toggled successfully"
    try:
        is_streaming = video_stream.toggle_stream()
    except Excetion as e:
        successful = False
        message = str(e)
    return jsonify({
        'status': 'success' if successful else 'error',
        'streaming': is_streaming if successful else False,
        'message': message
    })
  
@routes.route('/sensor-data')
def sensor_data():
    """Server-Sent Events endpoint for live sensor data."""
    def generate():
        while True:
            try:
                data = sensor_interface.get_latest_data()
                if data:
                    yield f"data: {json.dumps(data)}\n\n"
                time.sleep(0.5)  # Adjust sampling rate as needed
            except Exception as e:
                print(f"Error in sensor-data SSE: {e}")
                yield "data: {}\n\n"
    return Response(generate(), mimetype='text/event-stream')
