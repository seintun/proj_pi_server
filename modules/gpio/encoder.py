import numpy as np
from gpiozero import DigitalInputDevice
import time

# Configuration
LEFT_ENCODER_PIN = 5
RIGHT_ENCODER_PIN = 6

# Temporary counters
left_count = np.uint32(0)
right_count = np.uint32(0)

def left_encoder_callback():
    global left_count
    left_count += 1

def right_encoder_callback():
    global right_count
    right_count += 1

# Setup encoders with hardware interrupts
left_encoder = DigitalInputDevice(LEFT_ENCODER_PIN, pull_up=True, bounce_time=0.01)
right_encoder = DigitalInputDevice(RIGHT_ENCODER_PIN, pull_up=True, bounce_time=0.01)
left_encoder.when_activated = left_encoder_callback
right_encoder.when_activated = right_encoder_callback

def vehicle_path(L, R, path) -> np.ndarray:
    x, y, theta = path[-1]  # Get the last state
    wheel_diameter = 0.065  # meters
    wheel_radius = wheel_diameter/2
    wheel_distance = 0.15  # meters
    encoder_slots = 20  # number of slots on the encoder
    dist_center = 0.1  # Distance from the center of the robot to the wheel contatct point
    dw = wheel_distance / 2
    dL = (L / encoder_slots) * (2 * np.pi * wheel_radius)
    dR = (R / encoder_slots) * (2 * np.pi * wheel_radius)
    distance = (dL + dR) / 2
    real_distance = distance + dist_center
    delta_theta = (dR - dL) / (2 * dw)

    # Use the absolute motion model
    x += real_distance * np.cos(theta + delta_theta / 2)
    y += real_distance * np.sin(theta + delta_theta / 2)
    theta += delta_theta

    # Append the new state to the path
    path = np.vstack((path, [x, y, theta]))
    return path

path = np.array([[0, 0, 0]])  # x, y, theta

try:
    while True:
        # Update the path with the latest encoder counts
        path = vehicle_path(left_count, right_count, path)
        left_count = right_count = np.uint32(0)  # Reset counters
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Silent exit on Ctrl+C
finally:
    left_encoder.close()
    right_encoder.close()
