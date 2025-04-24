import psutil
from ..utils.circular_buffer import CircularBuffer

class MemoryMonitor:
    def __init__(self):
        self.usage_buffer = CircularBuffer()
        self._last_memory = 0
    
    def get_usage(self):
        """Get current RAM usage percentage"""
        try:
            memory = psutil.virtual_memory()
            self._last_memory = memory.percent
            self.usage_buffer.add(self._last_memory)
            return self._last_memory
        except Exception as e:
            print(f"Error reading memory usage: {e}")
            return self._last_memory
    
    def get_history(self):
        """Get historical memory usage data"""
        return self.usage_buffer.get_all()
    
    def get_detailed_info(self):
        """Get detailed memory information"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent
            }
        except Exception as e:
            print(f"Error reading detailed memory info: {e}")
            return None
