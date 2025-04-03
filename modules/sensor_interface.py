from typing import Dict, Optional, List
import time
import threading
from queue import Queue
import json
import RPi.GPIO as GPIO # For updated code below
import random

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
                ultrasonic_reading = self._read_ultrasonic_sensor()
                lidar_reading = self._read_lidar_sensor()
                
                with self._lock:
                    self.sensor_data.update({
                        'ultrasonic': ultrasonic_reading,
                        'lidar': lidar_reading
                    })
                
                print(f"Ultrasonic Reading: {ultrasonic_reading}")  # Debug log
                print(f"Lidar Reading: {lidar_reading}")  # Debug log
                # Add to queue for processing
                # if not self.data_queue.full():
                #     self.data_queue.put(ultrasonic_reading)
                #     self.data_queue.put(lidar_reading)
                
                time.sleep(1)  # Adjust sampling rate as needed
                
            except Exception as e:
                print(f"Error collecting sensor data: {e}")
                time.sleep(1)  # Wait before retrying

    def _read_ultrasonic_sensor(self) -> Dict[str, float]:
        """Read data from distance sensor.
        
        TODO: Implement actual sensor reading logic using GPIO
        This is a placeholder that returns dummy data.
        """
        return {
            'distance': round(random.uniform(10.0, 100.0), 2),  # Simulate distance between 10cm and 100cm
            'timestamp': time.time()
        }
    
    def _read_lidar_sensor(self) -> Dict[str, float]:
        """Simulate reading data from a lidar sensor."""
        return {
            'distance': round(random.uniform(50.0, 200.0), 2),  # Simulate distance between 50cm and 200cm
            'timestamp': time.time()
        }

    def get_latest_data(self) -> Dict[str, float]:
        """Get the most recent sensor reading."""
        with self._lock:
            print(f"Latest sensor data: {self.sensor_data}")  # Debug log
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

# Updated code below:
# class SensorInterface:
#     def __init__(self):
#         self.sensor_data = {}
#         self.data_queue = Queue(maxsize=100)
#         self.is_collecting = False
#         self._collection_thread = None
#         self._lock = threading.Lock()

#         # GPIO setup for ultrasonic sensor
#         self.TRIG_PIN = 23  # Replace with your actual GPIO pin for TRIG
#         self.ECHO_PIN = 24  # Replace with your actual GPIO pin for ECHO
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.TRIG_PIN, GPIO.OUT)
#         GPIO.setup(self.ECHO_PIN, GPIO.IN)

#     def _read_distance_sensor(self) -> Dict[str, float]:
#         """Read data from the ultrasonic distance sensor."""
#         try:
#             # Send a 10us pulse to trigger the sensor
#             GPIO.output(self.TRIG_PIN, True)
#             time.sleep(0.00001)  # 10 microseconds
#             GPIO.output(self.TRIG_PIN, False)

#             # Wait for the echo to start
#             while GPIO.input(self.ECHO_PIN) == 0:
#                 pulse_start = time.time()

#             # Wait for the echo to end
#             while GPIO.input(self.ECHO_PIN) == 1:
#                 pulse_end = time.time()

#             # Calculate the distance
#             pulse_duration = pulse_end - pulse_start
#             distance = pulse_duration * 17150  # Speed of sound: 34300 cm/s divided by 2
#             distance = round(distance, 2)  # Round to 2 decimal places

#             return {
#                 'distance': distance,  # Distance in cm
#                 'timestamp': time.time()
#             }
#         except Exception as e:
#             print(f"Error reading distance sensor: {e}")
#             return {
#                 'distance': -1,  # Indicate an error with -1
#                 'timestamp': time.time()
#             }

# # Create a single instance to be used across the application
# sensor_interface = SensorInterface()

# Latest update below
# def _read_distance_sensor(self) -> Dict[str, float]:
#     """Read data from ultrasonic distance sensor."""
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(self.TRIG_PIN, GPIO.OUT)
#     GPIO.setup(self.ECHO_PIN, GPIO.IN)

#     # Send a 10us pulse to trigger
#     GPIO.output(self.TRIG_PIN, True)
#     time.sleep(0.00001)
#     GPIO.output(self.TRIG_PIN, False)

#     # Measure the time for the echo
#     while GPIO.input(self.ECHO_PIN) == 0:
#         pulse_start = time.time()
#     while GPIO.input(self.ECHO_PIN) == 1:
#         pulse_end = time.time()

#     pulse_duration = pulse_end - pulse_start
#     distance = pulse_duration * 17150  # Convert to cm
#     distance = round(distance, 2)

#     return {
#         'distance': distance,
#         'timestamp': time.time()
#     }