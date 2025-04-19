from .cpu import CPUMonitor
from .memory import MemoryMonitor
from .temperature import TemperatureMonitor
from .system_info import get_cpu_info, get_memory_info, format_memory_size
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
        """Get current values with detailed system information"""
        # Get CPU information
        cpu_info = get_cpu_info()
        cpu_info['usage'] = self.cpu.get_usage()
        
        # Get memory information with percentage
        memory_info = get_memory_info()
        memory_usage = self.memory.get_usage()  # Get current usage percentage
        
        # Convert to human readable format
        memory_info['total_formatted'] = format_memory_size(memory_info['total'])
        memory_info['used_formatted'] = format_memory_size(memory_info['used'])
        memory_info['free_formatted'] = format_memory_size(memory_info['free'])
        memory_info['percent'] = memory_usage  # Ensure percentage is included
        
        return {
            'cpu': cpu_info,
            'memory': memory_info,
            'temperature': self.temperature.get_temperature()
        }
