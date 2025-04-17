document.addEventListener("DOMContentLoaded", function () {
    const ultrasonicSensorElement = document.getElementById("ultrasonicSensor");
    const lidarSensorElement = document.getElementById("lidarSensor");

    if (!ultrasonicSensorElement || !lidarSensorElement) {
        console.error("Element with id 'ultrasonicSensor' or 'lidarSensor' not found in the DOM.");
        return;
    }

    // Connect to the SSE endpoint
    const eventSource = new EventSource("/sensor-data");

    eventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);

        // Update the ultrasonic sensor data
        if (data.ultrasonic) {
            if (data.ultrasonic.distance === "Out of range") {
                ultrasonicSensorElement.textContent = "Out of range";
            } else {
                ultrasonicSensorElement.textContent = `${data.ultrasonic.distance} cm`;
            }
        }

        // Update the lidar sensor data
        if (data.lidar) {
            if (data.lidar.distance === "Out of range") {
                lidarSensorElement.textContent = "Out of range";
            } else {
                lidarSensorElement.textContent = `${data.lidar.distance} cm`;
            }
        }
    };

    eventSource.onerror = function () {
        ultrasonicSensorElement.textContent = "Error: Unable to fetch sensor data.";
        lidarSensorElement.textContent = "Error: Unable to fetch sensor data.";
    };
});