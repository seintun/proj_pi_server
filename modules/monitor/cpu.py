import psutil
from ..utils.circular_buffer import CircularBuffer

class CPUMonitor:
    def __init__(self):
        self.usage_buffer = CircularBuffer()
        self._last_cpu = 0
    
    def get_usage(self):
        """Get current CPU usage percentage"""
        try:
            usage = psutil.cpu_percent(interval=None)
            # Only update if we got a valid reading
            if usage != 0:
                self._last_cpu = usage
            self.usage_buffer.add(self._last_cpu)
            return self._last_cpu
        except Exception as e:
            print(f"Error reading CPU usage: {e}")
            return self._last_cpu
    
    def get_history(self):
        """Get historical CPU usage data"""
        return self.usage_buffer.get_all()
