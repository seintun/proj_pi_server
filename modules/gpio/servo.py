import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class servoControl:
    def __init__(self, pwm_chip, pwm_channel, gpio_name, initial_position):
        # Check if required parameters are valid
        if not pwm_chip or not pwm_channel or not gpio_name:
            logger.warning(f"Invalid parameters for servo: pwm_chip={pwm_chip}, pwm_channel={pwm_channel}, gpio_name={gpio_name}. Servo functionality disabled.")
            self.enabled = False
            return

        self.enabled = True

        # Define positions of the servos
        # Typical range is 500000 (0°) to 2500000 (180°)
        self.up_position = 1600000
        self.down_position = 1300000
        self.closed_position = 2400000
        self.opened_position = 1500000
        self.current_position_arm = initial_position
        self.current_position_gripper = initial_position

        self.pwm_chip = pwm_chip
        self.pwm_channel = pwm_channel
        self.gpio_name = gpio_name
        self.pwm_path = f"{pwm_chip}/{pwm_channel}"
        self.PWM_PERIOD = 20000000  # 20ms period (50Hz frequency)

        try:
            # Initialize the PWM channel
            self.export_pwm()
            self.set_period(self.PWM_PERIOD)
            self.enable_pwm()

            # Move to initial position
            self.set_duty_cycle(initial_position)

            time.sleep(0.5)  # Give time to reach position
        except Exception as e:
            logger.error(f"Failed to initialize servo {gpio_name}: {e}")
            self.enabled = False

    def export_pwm(self):
        if not self.enabled:
            return
        channel_number = self.pwm_channel.replace("pwm", "")
        if not os.path.exists(self.pwm_path):
            with open(f"{self.pwm_chip}/export", "w") as f:
                f.write(channel_number)
            time.sleep(0.1)
            while not os.path.exists(self.pwm_path):
                time.sleep(0.1)

    def set_period(self, period_ns):
        if not self.enabled:
            return
        try:
            with open(f"{self.pwm_path}/period", "w") as f:
                f.write(str(period_ns))
        except IOError as e:
            print(f"Error setting period on {self.pwm_path}: {e}")
            raise

    def set_duty_cycle(self, duty_ns):
        if not self.enabled:
            return
        with open(f"{self.pwm_path}/duty_cycle", "w") as f:
            f.write(str(duty_ns))

    def enable_pwm(self):
        if not self.enabled:
            return
        with open(f"{self.pwm_path}/enable", "w") as f:
            f.write("1")

    def smooth_move(self, start, end, steps=10, delay=0.02):
        if not self.enabled:
            logger.warning("Servo functionality is disabled. Cannot perform smooth_move.")
            return
        step_size = (end - start) // steps
        for i in range(steps + 1):
            try:
                self.set_duty_cycle(start + i * step_size)
                time.sleep(delay)
            except IOError as e:
                print(f"Error during smooth_move on {self.pwm_path}: {e}")
                raise

    def arm_up(self):
        if not self.enabled:
            logger.warning("Servo functionality is disabled. Cannot move arm up.")
            return
        self.smooth_move(self.current_position_arm, self.up_position)
        self.current_position_arm = self.up_position

    def arm_down(self):
        if not self.enabled:
            logger.warning("Servo functionality is disabled. Cannot move arm down.")
            return
        self.smooth_move(self.current_position_arm, self.down_position)
        self.current_position_arm = self.down_position

    def close_gripper(self):
        if not self.enabled:
            logger.warning("Servo functionality is disabled. Cannot close gripper.")
            return
        self.smooth_move(self.current_position_gripper, self.closed_position)
        self.current_position_gripper = self.closed_position

    def open_gripper(self):
        if not self.enabled:
            logger.warning("Servo functionality is disabled. Cannot open gripper.")
            return
        self.smooth_move(self.current_position_gripper, self.opened_position)
        self.current_position_gripper = self.opened_position

    def __del__(self):
        if not self.enabled:
            return
        with open(f"{self.pwm_path}/enable", "w") as f:
            f.write("0")

        channel_number = self.pwm_channel.replace("pwm", "")
        with open(f"{self.pwm_chip}/unexport", "w") as f:
            f.write(channel_number)

servo_arm = servoControl(
    pwm_chip="/sys/class/pwm/pwmchip2",
    pwm_channel="pwm2",
    gpio_name="GPIO18",
    initial_position=1300000
)

servo_gripper = servoControl(
    pwm_chip="/sys/class/pwm/pwmchip2",
    pwm_channel="pwm3",
    gpio_name="GPIO13",
    initial_position=1500000
)
