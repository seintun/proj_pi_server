from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/action', methods=['GET'])
def action():
    print("Button clicked! Performing Raspberry Pi action...")
    # Add your action here (e.g., turn on an LED, execute a script, etc.)
    return jsonify({"message": "Action executed on Raspberry Pi!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)