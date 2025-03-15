from flask import Blueprint, render_template, Response, send_file, jsonify
import json
import time
import os
from .monitor import SystemMonitor
from .video_stream import video_stream  # Import the singleton instance

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
        # Return a simple response with black background
        html = '''
        <html>
            <body style="margin:0;padding:0;background:#000;height:100%;width:100%;display:flex;align-items:center;justify-content:center;">
                <div style="color:#ffdb15;font-family:monospace;text-align:center;">
                    <div style="font-size:24px;margin-bottom:10px;">📷</div>
                    <div>No Camera Feed</div>
                </div>
            </body>
        </html>
        '''
        return Response(html, mimetype='text/html')

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
