import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

recognized_name = "Unknown"  # Default recognized name

@app.route('/get_name', methods=['GET'])
def get_name():
    return jsonify(name=recognized_name)

@app.route('/update_name', methods=['POST'])
def update_name():
    global recognized_name
    data = request.get_json()
    recognized_name = data['name']
    return jsonify(success=True, name=recognized_name)

@app.route('/start_main_script', methods=['POST'])
def start_main_script():
    try:
        # Get the full path to the Python executable
        python_executable = sys.executable
        subprocess.run([python_executable, 'main.py'])
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
