import logging
import time
from typing import Dict, Optional, List
import threading
from queue import Queue
import json
from gpiozero import DistanceSensor
import board
import busio
import adafruit_vl53l0x

# Configure logger
logger = logging.getLogger(__name__)

class SensorInterface:
    def __init__(self):
        self.sensor_data = {}
        self.data_queue = Queue(maxsize=100)
        self.is_collecting = False
        self._collection_thread = None
        self._lock = threading.Lock()
        self._lidar = None

        # Initialize the VL53L0X sensor
        try:
            logger.info("Initializing VL53L0X sensor...")
            i2c = busio.I2C(board.SCL, board.SDA)
            self._lidar = adafruit_vl53l0x.VL53L0X(i2c)
            self._lidar.measurement_timing_budget = 200000  # Optional: Set timing budget
            time.sleep(0.1)  # Allow sensor to stabilize
            logger.info("VL53L0X sensor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VL53L0X sensor: {e}")
            self._lidar = None

        # Start collection automatically upon initialization
        self.start_collection()
        logger.info("SensorInterface initialized and data collection started")

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
        interval = 0.5  # Match the interval with the data collector
        while self.is_collecting:
            try:
                # Real-time sensor readings
                ultrasonic_reading = self._read_ultrasonic_sensor()
                lidar_reading = self._read_lidar_sensor()

                # Check if ultrasonic sensor distance is greater than 100 cm
                if ultrasonic_reading['distance'] > 100:
                    lidar_reading['distance'] = "Out of range"

                with self._lock:
                    self.sensor_data.update({
                        'ultrasonic': ultrasonic_reading,
                        'lidar': lidar_reading
                    })

                logger.debug(f"Ultrasonic Reading: {ultrasonic_reading}")
                logger.debug(f"Lidar Reading: {lidar_reading}")

            except Exception as e:
                logger.error(f"Error collecting sensor data: {e}")

            time.sleep(interval)  # Adjusted interval

    def _read_ultrasonic_sensor(self) -> Dict[str, float]:
        """Read data from ultrasonic sensor using gpiozero"""
        
        TRIG_PIN = 16  # Replace with your actual TRIG pin number
        ECHO_PIN = 26  # Replace with your actual ECHO pin number

        try:
            # Set max_distance to 4.0 meters (400 cm)
            sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=9.0)
            raw_distance_1 = sensor.distance * 100  # Convert to cm
            raw_distance_2 = 1.0029 * raw_distance_1 + 0.2654
            distance = round(raw_distance_2, 2)

            # Check if the distance exceeds the maximum range
            if raw_distance_1 > 400:  # 400 cm is the max_distance in cm
                return {
                    'distance': "Out of range",
                    'timestamp': time.time()
                }
        except Exception as e:
            logger.error(f"Error reading ultrasonic sensor: {e}")
            distance = -1.0  # Indicate an error with a negative value

        return {
            'distance': distance,
            'timestamp': time.time()
        }

    def _read_lidar_sensor(self) -> Dict[str, float]:
        """Read data from VL53L0X lidar sensor."""
        if not self._lidar:
            logger.debug("Lidar sensor not initialized (_lidar is None)")
            return {
                'distance': -1.0,
                'timestamp': time.time()
            }

        try:
            logger.debug("Attempting to read distance from lidar...")
            distance_mm = self._lidar.range
            if distance_mm < 30 or distance_mm > 1000:  # Validate range (0-1000mm typical for VL53L0X)
                logger.warning(f"Invalid lidar reading: {distance_mm}mm")
                distance_mm = -1.0
            logger.debug(f"Validated distance reading: {distance_mm}mm")
            raw_distance_1 = distance_mm / 10  # Convert mm to cm
            raw_distance_2 = 6e-10 * raw_distance_1**6 - 2e-7 * raw_distance_1**5 + 3e-5 * raw_distance_1**4 - 0.0023 * raw_distance_1**3 + 0.0817 * raw_distance_1**2 - 0.3912 * raw_distance_1 + 4.7317
            distance = round(raw_distance_2, 2)
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
