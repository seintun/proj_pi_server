from typing import Dict, Optional, List
import time
import threading
from queue import Queue
import json
import random
import RPi.GPIO as GPIO

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
                
                print(f"Ultrasonic Reading: {ultrasonic_reading}")  # Debug log
                print(f"Lidar Reading: {lidar_reading}")  # Debug log
                
                time.sleep(0.5)  # Adjust sampling rate as needed
                
            except Exception as e:
                print(f"Error collecting sensor data: {e}")
                time.sleep(0.5)  # Wait before retrying

    def _read_ultrasonic_sensor(self) -> Dict[str, float]:
        """Read data from ultrasonic sensor using GPIO"""
        
        TRIG_PIN = 23  # Replace with your actual TRIG pin number
        ECHO_PIN = 24  # Replace with your actual ECHO pin number

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)

        # Send a 10us pulse to trigger the sensor
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        # Measure the time for the echo to return
        pulse_start = time.time()
        pulse_end = time.time()

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        # Calculate distance in cm
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        distance = round(distance, 2)

        # Cleanup GPIO
        GPIO.cleanup()

        return {
            'distance': distance,
            'timestamp': time.time()
        }
    
    def _read_lidar_sensor(self) -> Dict[str, float]:
        """Read dada from lidar sensor""" 
        try:
            import smbus
            # Replace with your actual I2C address and setup
            I2C_ADDRESS = 0x29  # Default I2C address for VL53L0X.
            bus = smbus.SMBus(1)  # Use I2C bus 1

            # Example: Read distance from VL53L0X
            # You will need to use the appropriate library or commands for your lidar sensor
            # This is a placeholder for actual lidar reading logic
            distance = random.uniform(50.0, 200.0)  # Replace with actual reading logic
            distance = round(distance, 2)

            return {
                'distance': distance,
                'timestamp': time.time()
            }
        except Exception as e:
            print(f"Error reading lidar sensor: {e}")
            return {
                'distance': 0.0,
                'timestamp': time.time()
            }

    def get_latest_data(self) -> Dict[str, float]:
        # Get the most recent sensor reading
        with self._lock:
            print(f"Latest sensor data: {self.sensor_data}")  # Debug log
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