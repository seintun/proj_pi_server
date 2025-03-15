import os
from ..utils.circular_buffer import CircularBuffer

class TemperatureMonitor:
    def __init__(self):
        self.temp_buffer = CircularBuffer()
        self._last_temp = 0
        self.temp_path = '/sys/class/thermal/thermal_zone0/temp'
    
    def get_temperature(self):
        """Get current CPU temperature in Celsius"""
        try:
            if os.path.exists(self.temp_path):
                with open(self.temp_path, 'r') as f:
                    # Convert millidegrees to degrees Celsius
                    temp = round(float(f.read()) / 1000.0, 1)
                    self._last_temp = temp
                    self.temp_buffer.add(temp)
                    return temp
            else:
                # If not running on Raspberry Pi, simulate temperature for testing
                import random
                temp = round(40 + random.uniform(-5, 5), 1)  # Simulate around 40°C
                self._last_temp = temp
                self.temp_buffer.add(temp)
                return temp
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return self._last_temp
    
    def get_history(self):
        """Get historical temperature data"""
        return self.temp_buffer.get_all()
    
    def is_critical(self):
        """Check if temperature is at critical level (> 80°C)"""
        current_temp = self.get_temperature()
        return current_temp > 80
