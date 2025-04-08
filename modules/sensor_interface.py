import logging
import time
from typing import Dict, Optional, List
import threading
from queue import Queue
import json
from gpiozero import DistanceSensor
import smbus  # For I2C communication

# Configure logger
logger = logging.getLogger(__name__)

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
                # Real-time sensor readings
                ultrasonic_reading = self._read_ultrasonic_sensor()
                lidar_reading = self._read_lidar_sensor()
                
                with self._lock:
                    self.sensor_data.update({
                        'ultrasonic': ultrasonic_reading,
                        'lidar': lidar_reading
                    })
                
                logger.debug(f"Ultrasonic Reading: {ultrasonic_reading}")
                logger.debug(f"Lidar Reading: {lidar_reading}")
                
            except Exception as e:
                logger.error(f"Error collecting sensor data: {e}")
                
            time.sleep(0.4)  # Wait before retrying

    def _read_ultrasonic_sensor(self) -> Dict[str, float]:
        """Read data from ultrasonic sensor using gpiozero"""
        
        TRIG_PIN = 16  # Replace with your actual TRIG pin number
        ECHO_PIN = 26  # Replace with your actual ECHO pin number

        try:
            sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)
            distance = sensor.distance * 100  # Convert to cm
            distance = round(distance, 2)
        except Exception as e:
            logger.error(f"Error reading ultrasonic sensor: {e}")
            distance = -1.0  # Indicate an error with a negative value

        return {
            'distance': distance,
            'timestamp': time.time()
        }
    
    def _read_lidar_sensor(self) -> Dict[str, float]:
        """Read data from lidar sensor using direct I2C communication."""
        I2C_ADDRESS = 0x29  # Default I2C address for VL53L0X
        RESULT_RANGE_STATUS = 0x14  # Register for range status
        SYSRANGE_START = 0x00  # Register to start ranging
        bus = smbus.SMBus(1)  # Use I2C bus 1

        try:
            # Initialize the sensor
            bus.write_byte_data(I2C_ADDRESS, 0x80, 0x01)
            bus.write_byte_data(I2C_ADDRESS, 0xFF, 0x01)
            bus.write_byte_data(I2C_ADDRESS, 0x00, 0x00)
            bus.write_byte_data(I2C_ADDRESS, 0x91, 0x3C)
            bus.write_byte_data(I2C_ADDRESS, 0x00, 0x01)
            bus.write_byte_data(I2C_ADDRESS, 0xFF, 0x00)
            bus.write_byte_data(I2C_ADDRESS, 0x80, 0x00)

            # Start ranging
            bus.write_byte_data(I2C_ADDRESS, SYSRANGE_START, 0x01)
            time.sleep(0.05)  # Wait for measurement

            # Read range result
            range_mm = bus.read_word_data(I2C_ADDRESS, RESULT_RANGE_STATUS + 10)
            distance = range_mm / 10.0  # Convert mm to cm
            distance = round(distance, 2)
        except Exception as e:
            logger.error(f"Error reading lidar sensor: {e}")
            distance = -1.0  # Indicate an error with a negative value

        return {
            'distance': distance,
            'timestamp': time.time()
        }

    def get_latest_data(self) -> Dict[str, float]:
        # Get the most recent sensor reading
        with self._lock:
            logger.debug(f"Latest sensor data: {self.sensor_data}")
            return self.sensor_data.copy()

    def get_data_batch(self, batch_size: int = 10) -> List[Dict[str, float]]:
        # Get a batch of recent sensor readings
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
