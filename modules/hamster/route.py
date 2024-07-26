from flask import Blueprint, render_template, request, jsonify
import os, json

current_dir = os.path.dirname(os.path.abspath(__file__))
hamster = Blueprint('hamster', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='static')

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

@hamster.route('/')
def index():
    return render_template('hamster.html')

@hamster.route('/api/current', methods=['GET', 'POST'])
def api_settings():
    if request.method == 'GET':
        global settings
        settings = read_json(os.path.join(current_dir, 'hamsterkombat/current.json'))
        return jsonify(settings)
