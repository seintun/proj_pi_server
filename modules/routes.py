from flask import Blueprint, render_template, Response, send_file, jsonify, request
import json
import time
import os
import logging
from .monitor import SystemMonitor
from .video_stream import video_stream  # Import the singleton instance
from .gpio import motor_controller, servo_arm, servo_gripper, mp3_player

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
    
@routes.route('/api/gpio/motor/forward', methods=['POST'])
def forward():
    motor_controller.forward()
    return '', 200

@routes.route('/api/gpio/motor/backward', methods=['POST'])
def backward():
    motor_controller.backward()
    return '', 200

@routes.route('/api/gpio/motor/left', methods=['POST'])
def left():
    motor_controller.left()
    return '', 200

@routes.route('/api/gpio/motor/right', methods=['POST'])
def right():
    motor_controller.right()
    return '', 200

@routes.route('/api/gpio/motor/stop', methods=['POST'])
def stop():
    motor_controller.stop()
    return '', 200

@routes.route('/api/gpio/servo/up', methods=['POST'])
def up():
    servo_arm.arm_up()
    return '', 200

@routes.route('/api/gpio/servo/down', methods=['POST'])
def down():
    servo_arm.arm_down()
    return '', 200

@routes.route('/api/gpio/servo/close', methods=['POST'])
def close():
    servo_gripper.close_gripper()
    return '', 200

@routes.route('/api/gpio/servo/open', methods=['POST'])
def open():
    servo_gripper.open_gripper()
    return '', 200

@routes.route('/api/gpio/player/sayhello', methods=['POST'])
def play_hello():
    mp3_player.play_song_one()
    return '', 200

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

@routes.route('/video/toggle', methods=['POST'])
def toggle_video():
    """Toggle video stream on/off"""
    try:
        is_streaming = video_stream.toggle_stream()
        return jsonify({
            'status': 'success',
            'streaming': is_streaming,
            'message': 'Video stream toggled successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'streaming': False,
            'message': str(e)
        }), 503
