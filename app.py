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

if __name__ == '__main__':
    app = create_app()
    try:
        logger.info("Starting Robot Control Dashboard...")
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
