from flask import Flask
from modules.routes import routes
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(routes)
    
    # Configure app
    app.config.update(
        TEMPLATES_AUTO_RELOAD=True,  # Enable template auto-reload
        SEND_FILE_MAX_AGE_DEFAULT=0  # Prevent caching of static files during development
    )
    
    @app.after_request
    def add_header(response):
        """Add headers to prevent caching for SSE"""
        if 'text/event-stream' in response.content_type:
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['X-Accel-Buffering'] = 'no'
        return response
    
    return app

app = create_app()
try:
    host = '0.0.0.0'
    port = 5000
    logger.info(f"Starting Robot Control Dashboard at http://{host}:{port}")
    app.run(host=host, port=port, threaded=True, debug=True)  # Enable debug mode
except KeyboardInterrupt:
    logger.info("Shutting down gracefully...")
    from modules.video_stream import video_stream
    from modules.gpio.motor import motor_controller
    from modules.gpio.servo import servo_arm, servo_gripper

    # Cleanup video stream
    video_stream.cleanup()

    # Cleanup motor controller
    # motor_controller.cleanup()

    # Cleanup servo controllers
    servo_arm.cleanup()
    servo_gripper.cleanup()

    logger.info("Resources cleaned up. Exiting.")
except Exception as e:
    logger.error(f"Error starting server: {e}")
