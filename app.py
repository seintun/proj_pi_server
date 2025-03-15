from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)

# Use OpenCV with Raspberry Pi camera module or USB webcam
camera = cv2.VideoCapture(0)  # Change to 1 if using an external USB camera

is_streaming = True  # Video stream toggle state


def generate_frames():
    """ Continuously capture frames and stream them. """
    while is_streaming:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Yield frame as a response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    """ Serve the HTML page with video stream and buttons. """
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """ Route for streaming the video feed. """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/toggle_stream', methods=['POST'])
def toggle_stream():
    """ Toggle video streaming on/off. """
    global is_streaming
    is_streaming = not is_streaming
    return jsonify({"streaming": is_streaming})


@app.route('/action', methods=['GET'])
def action():
    """ Custom Raspberry Pi action (e.g., turn on LED). """
    print("Button clicked! Performing Raspberry Pi action...")
    # Example: Run a script, turn on LED, etc.
    return jsonify({"message": "Action executed on Raspberry Pi!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Disable debug for better performance
