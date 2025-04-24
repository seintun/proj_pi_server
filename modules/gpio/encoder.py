import numpy as np
from gpiozero import DigitalInputDevice
from .motor import motor_controller  # Import the singleton instance

class EncoderTracker:
    def __init__(self, left_pin=5, right_pin=6):
        # Configuration
        self.left_encoder_pin = left_pin
        self.right_encoder_pin = right_pin

        # Temporary counters
        self.left_count = np.uint32(0)
        self.right_count = np.uint32(0)

        # Path tracking
        self.path = np.array([[0, 0, (np.pi/2)]])  # x, y, theta

        # Setup encoders with hardware interrupts
        self.left_encoder = DigitalInputDevice(self.left_encoder_pin, pull_up=True, bounce_time=0.001)
        self.right_encoder = DigitalInputDevice(self.right_encoder_pin, pull_up=True, bounce_time=0.001)
        self.left_encoder.when_activated = self.left_encoder_callback
        self.right_encoder.when_activated = self.right_encoder_callback

    def left_encoder_callback(self):
        self.left_count += 1

    def right_encoder_callback(self):
        self.right_count += 1

    def vehicle_path(self):
        x, y, theta = self.path[-1]  # Get the last state

        if self.left_count > 0 or self.right_count > 0:  # Only update if we have new counts
            wheel_diameter = 0.065  # meters
            wheel_radius = wheel_diameter / 2
            wheel_distance = 0.15  # meters
            encoder_slots = 20  # number of slots on the encoder
            dist_center = 0.1  # Distance from the center of the robot to the wheel contact point
            dw = wheel_distance / 2

            # Get current motor directions from motor_controller
            left_dir, right_dir = motor_controller.get_current_directions()

            # Calculate distances with direction
            dL = (self.left_count / encoder_slots) * (2 * np.pi * wheel_radius) * left_dir
            dR = (self.right_count / encoder_slots) * (2 * np.pi * wheel_radius) * right_dir
            distance = (dL + dR) / 2
            delta_theta = (dR - dL) / (2 * dw)

            # Update position
            x += distance * np.cos(theta + (delta_theta / 2))
            y += distance * np.sin(theta + (delta_theta / 2))
            theta += delta_theta

            # Append the new state to the path
            self.path = np.vstack((self.path, [x, y, theta]))
            
            # Reset encoder counts
            self.left_count = self.right_count = np.uint32(0)

        return x, y, theta  # Always return current position

    def get_position(self):
        """Get the latest x, y position."""
        return self.path[-1][:2]  # Return only x and y

    def update_path(self):
        self.vehicle_path()

    def __del__(self):
        self.left_encoder.close()
        self.right_encoder.close()

# Initialize the encoder tracker
encoder_tracker = EncoderTracker()