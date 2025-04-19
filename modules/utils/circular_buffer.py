from collections import deque
from threading import Lock
import time

class CircularBuffer:
    def __init__(self, size=60):
        self.buffer = deque(maxlen=size)
        self.lock = Lock()
        self.last_update = 0
        self.update_threshold = 0.5  # 500ms minimum between updates
    
    def add(self, item):
        current_time = time.time()
        with self.lock:
            if current_time - self.last_update >= self.update_threshold:
                self.buffer.append(item)
                self.last_update = current_time
    
    def get_all(self):
        with self.lock:
            return list(self.buffer)
    
    def get_latest(self):
        with self.lock:
            return self.buffer[-1] if self.buffer else None
    
    def clear(self):
        with self.lock:
            self.buffer.clear()
