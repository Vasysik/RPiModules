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

@hamster.route('/api/current', methods=['GET'])
def api_current():
    return jsonify(read_json(os.path.join(current_dir, 'current.json')))

@hamster.route('/api/current/<user>/<element>', methods=['GET'])
def api_current_user_element(user, element):
    data = read_json(os.path.join(current_dir, 'current.json'))
    user_data = data.get(user, {})
    element_value = user_data.get(element, None)

    if element_value is None:
        return jsonify({"error": "Element not found"}), 404

    return jsonify({element: element_value})

@hamster.route('/api/status', methods=['GET'])
def api_status():
    return jsonify(read_json(os.path.join(current_dir, 'status.json')))

@hamster.route('/api/config', methods=['GET'])
def api_config():
    return jsonify(read_json(os.path.join(current_dir, 'config.json')))

@hamster.route('/api/tokens', methods=['GET', 'POST', 'DELETE'])
def api_tokens():
    tokens_file = os.path.join(current_dir, 'tokens.txt')
    
    if request.method == 'GET':
        if os.path.exists(tokens_file):
            with open(tokens_file, 'r') as f:
                tokens = [line.strip() for line in f.readlines()]
            return jsonify(tokens)
        return jsonify([])
    
    elif request.method == 'POST':
        token = request.json.get('token')
        if token:
            with open(tokens_file, 'a') as f:
                f.write(f"{token}\n")
            return jsonify({"message": "Token added successfully"}), 201
        return jsonify({"error": "Invalid token"}), 400
    
    elif request.method == 'DELETE':
        token = request.json.get('token')
        if token:
            with open(tokens_file, 'r') as f:
                tokens = f.readlines()
            with open(tokens_file, 'w') as f:
                f.writelines([line for line in tokens if line.strip() != token])
            return jsonify({"message": "Token removed successfully"}), 200
        return jsonify({"error": "Invalid token"}), 400