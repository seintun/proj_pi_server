from gpiozero import PWMOutputDevice

# Define motor control class
class motorControl:
    def __init__(self):
        # Define speed variable
        self.speed = 1
        self.right_motor_forward = PWMOutputDevice(17)
        self.right_motor_backward = PWMOutputDevice(27)
        self.left_motor_forward = PWMOutputDevice(23)
        self.left_motor_backward = PWMOutputDevice(22)
        self.left_motor_direction = 0  # Initialize instance variable
        self.right_motor_direction = 0  # Initialize instance variable
        # Correct for hardware configuration
        self.correction_right = 1.0
        self.correction_left = 1.0
        # Calculate actual speed for each motor
        self.actual_speed_right = self.speed * self.correction_right #30rpm
        self.actual_speed_left = self.speed * self.correction_left #30rpm

        self.stop()

    def stop(self):
        self.right_motor_forward.value = 0
        self.right_motor_backward.value = 0
        self.left_motor_forward.value = 0
        self.left_motor_backward.value = 0
        self.left_motor_direction = 0
        self.right_motor_direction = 0

    def forward(self):
        self.right_motor_forward.value = self.actual_speed_right
        self.left_motor_forward.value = self.actual_speed_left
        self.right_motor_backward.value = 0
        self.left_motor_backward.value = 0
        self.left_motor_direction = 1
        self.right_motor_direction = 1
    
    def backward(self):
        self.right_motor_backward.value = self.actual_speed_right
        self.left_motor_backward.value = self.actual_speed_left
        self.right_motor_forward.value = 0
        self.left_motor_forward.value = 0
        self.left_motor_direction = -1
        self.right_motor_direction = -1
    
    def right(self):
        self.right_motor_backward.value = self.actual_speed_right
        self.left_motor_forward.value = self.actual_speed_left
        self.right_motor_forward.value = 0
        self.left_motor_backward.value = 0
        self.left_motor_direction = 1
        self.right_motor_direction = -1
    
    def left(self):
        self.right_motor_forward.value = self.actual_speed_right
        self.left_motor_backward.value = self.actual_speed_left
        self.right_motor_backward.value = 0
        self.left_motor_forward.value = 0
        self.left_motor_direction = -1
        self.right_motor_direction = 1

    def get_current_directions(self):
        """Get current motor directions"""
        return self.left_motor_direction, self.right_motor_direction

# Create singleton instance
motor_controller = motorControl()
