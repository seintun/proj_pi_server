from .cpu import CPUMonitor
from .memory import MemoryMonitor
from .temperature import TemperatureMonitor
import time

class SystemMonitor:
    def __init__(self):
        self.cpu = CPUMonitor()
        self.memory = MemoryMonitor()
        self.temperature = TemperatureMonitor()
        self.last_update = 0
        self.update_interval = 0.5  # 500ms minimum between updates
    
    def get_stats(self):
        """Get current system statistics"""
        current_time = time.time()
        
        # Throttle updates
        if current_time - self.last_update < self.update_interval:
            return None
            
        self.last_update = current_time
        
        return {
            'cpu': {
                'usage': self.cpu.get_usage(),
                'history': self.cpu.get_history()
            },
            'memory': {
                'usage': self.memory.get_usage(),
                'history': self.memory.get_history(),
                'details': self.memory.get_detailed_info()
            },
            'temperature': {
                'value': self.temperature.get_temperature(),
                'history': self.temperature.get_history(),
                'is_critical': self.temperature.is_critical()
            },
            'timestamp': current_time
        }
    
    def get_minimal_stats(self):
        """Get current values only without history for lighter payload"""
        return {
            'cpu_usage': self.cpu.get_usage(),
            'ram_usage': self.memory.get_usage(),
            'temperature': self.temperature.get_temperature()
        }
