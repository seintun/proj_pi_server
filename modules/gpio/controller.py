import logging
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPIOController:
    def __init__(self):
        """Initialize controller with simulated LED state"""
        self.led_state = False
        logger.info("GPIO Controller initialized (simulated mode)")
    
    def toggle_led(self):
        """Simulate LED toggle and return JSON response"""
        self.led_state = not self.led_state
        status = 'ON' if self.led_state else 'OFF'
        message = f"LED toggled: {status}"
        logger.info(message)
        return {
            'status': 'success',
            'message': message,
            'led_state': self.led_state
        }
    
    def cleanup(self):
        """Simulate cleanup"""
        logger.info("GPIO cleanup completed (simulated mode)")

# Create singleton instance
gpio_controller = GPIOController()

# Register cleanup on exit
import atexit
atexit.register(gpio_controller.cleanup)
