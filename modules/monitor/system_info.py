import psutil
import logging

logger = logging.getLogger(__name__)

def get_cpu_info():
    """Get CPU information with error handling"""
    try:
        return {
            'cores': psutil.cpu_count(logical=False) or 0,
            'threads': psutil.cpu_count(logical=True) or 0,
            'frequency': round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else 0
        }
    except Exception as e:
        logger.error(f"Error getting CPU info: {e}")
        return {
            'cores': 0,
            'threads': 0,
            'frequency': 0
        }

def get_memory_info():
    """Get memory information with error handling"""
    try:
        memory = psutil.virtual_memory()
        return {
            'total': round(memory.total / (1024 * 1024), 2),  # MB
            'used': round(memory.used / (1024 * 1024), 2),    # MB
            'free': round(memory.free / (1024 * 1024), 2),    # MB
            'percent': memory.percent
        }
    except Exception as e:
        logger.error(f"Error getting memory info: {e}")
        return {
            'total': 0,
            'used': 0,
            'free': 0,
            'percent': 0
        }

def format_memory_size(size_mb):
    """Convert MB to a human-readable format"""
    if size_mb > 1024:
        return f"{round(size_mb/1024, 2)} GB"
    return f"{round(size_mb, 2)} MB"
