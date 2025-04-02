from gpiozero import PWMOutputDevice

# Define speed variable
speed = 0.8

class motorControl:
    def __init__(self):
        self.right_motor_forward = PWMOutputDevice(17)
        self.right_motor_backward = PWMOutputDevice(27)
        self.left_motor_forward = PWMOutputDevice(23)
        self.left_motor_backward = PWMOutputDevice(22)
        self.stop()

    def stop(self):
        self.right_motor_forward.value = 0
        self.right_motor_backward.value = 0
        self.left_motor_forward.value = 0
        self.left_motor_backward.value = 0

    def forward(self):
        self.right_motor_forward.value = speed
        self.left_motor_forward.value = speed
    
    def backward(self):
        self.right_motor_backward.value = speed
        self.left_motor_backward.value = speed
    
    def right(self):
        self.right_motor_backward.value = speed
        self.left_motor_forward.value = speed
    
    def left(self):
        self.right_motor_forward.value = speed
        self.left_motor_backward.value = speed

# Create singleton instance
motor_controller = motorControl()
