from flask import Flask
from modules.routes import routes
import os

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(routes)
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Ensure the static and templates directories exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False  # Disable debug for better performance
    )
