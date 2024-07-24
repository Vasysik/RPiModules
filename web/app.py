from flask import Flask, render_template
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

app = Flask(__name__)

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

modules_paths = read_json(os.path.join(current_dir, "modules_paths.json"))

from modules.fan_control.route import fan_control
app.register_blueprint(fan_control, url_prefix='/fan_control')

@app.route('/')
def index():
    return render_template('base_layout.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)