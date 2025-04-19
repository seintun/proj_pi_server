import csv
import time
import threading
import os
from datetime import datetime
from .gpio.encoder import encoder_tracker
from .sensor_interface import sensor_interface

class DataCollector:
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.csv_file_path = None
        self.is_collecting = False
        self._collection_thread = None

    def _generate_file_path(self):
        """Generate a unique file path based on the current date and time."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return os.path.join(self.base_folder, f"{timestamp}.csv")

    def start_collection(self, interval=0.5):
        """Start collecting data at a fixed interval."""
        if not self.is_collecting:
            self.is_collecting = True
            self.csv_file_path = self._generate_file_path()

            # Ensure the training folder exists
            os.makedirs(self.base_folder, exist_ok=True)

            # Initialize the CSV file with headers
            with open(self.csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp', 'x', 'y', 'ultrasonic', 'lidar'])

            self._collection_thread = threading.Thread(target=self._collect_data, args=(interval,))
            self._collection_thread.daemon = True
            self._collection_thread.start()

    def stop_collection(self):
        """Stop collecting data."""
        self.is_collecting = False
        if self._collection_thread:
            self._collection_thread.join()

    def _collect_data(self, interval):
        """Collect data from the robot's position and sensors."""
        while self.is_collecting:
            try:
                # Get robot position
                x, y = encoder_tracker.get_position()

                # Get sensor data
                sensor_data = sensor_interface.get_latest_data()
                ultrasonic = sensor_data.get('ultrasonic', {}).get('distance', -1)
                lidar = sensor_data.get('lidar', {}).get('distance', -1)

                # Get the current time in HH:MM:SS format
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Write data to CSV
                with open(self.csv_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, x, y, ultrasonic, lidar])

            except Exception as e:
                print(f"Error collecting data: {e}")

            time.sleep(interval)

# Initialize the data collector with the training folder
data_collector = DataCollector('/home/ArthurPI5/Projects/GitHub/proj_pi_server/modules/training')
