from typing import Dict, Optional, List
import time
import threading
from queue import Queue
import json

class SensorInterface:
    def __init__(self):
        self.sensor_data = {}
        self.data_queue = Queue(maxsize=100)
        self.is_collecting = False
        self._collection_thread = None
        self._lock = threading.Lock()

    def start_collection(self) -> None:
        """Start collecting sensor data in a separate thread."""
        if not self.is_collecting:
            self.is_collecting = True
            self._collection_thread = threading.Thread(target=self._collect_data)
            self._collection_thread.daemon = True
            self._collection_thread.start()

    def stop_collection(self) -> None:
        """Stop collecting sensor data."""
        self.is_collecting = False
        if self._collection_thread:
            self._collection_thread.join()

    def _collect_data(self) -> None:
        """Continuously collect data from sensors."""
        while self.is_collecting:
            try:
                # Placeholder for actual sensor reading logic
                # TODO: Implement actual sensor reading here
                sensor_reading = self._read_distance_sensor()
                
                with self._lock:
                    self.sensor_data.update(sensor_reading)
                
                # Add to queue for processing
                if not self.data_queue.full():
                    self.data_queue.put(sensor_reading)
                
                time.sleep(0.1)  # Adjust sampling rate as needed
                
            except Exception as e:
                print(f"Error collecting sensor data: {e}")
                time.sleep(1)  # Wait before retrying

    def _read_distance_sensor(self) -> Dict[str, float]:
        """Read data from distance sensor.
        
        TODO: Implement actual sensor reading logic using GPIO
        This is a placeholder that returns dummy data.
        """
        return {
            'distance': 0.0,  # Distance in cm
            'timestamp': time.time()
        }

    def get_latest_data(self) -> Dict[str, float]:
        """Get the most recent sensor reading."""
        with self._lock:
            return self.sensor_data.copy()

    def get_data_batch(self, batch_size: int = 10) -> List[Dict[str, float]]:
        """Get a batch of recent sensor readings."""
        batch = []
        while len(batch) < batch_size and not self.data_queue.empty():
            batch.append(self.data_queue.get())
        return batch

    def export_data(self, filepath: str) -> None:
        """Export collected data to JSON file."""
        with self._lock:
            with open(filepath, 'w') as f:
                json.dump(self.sensor_data, f)

    def __del__(self):
        """Ensure clean shutdown of data collection."""
        self.stop_collection()

# Create a single instance to be used across the application
sensor_interface = SensorInterface()
