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

config = read_json(os.path.join(current_dir, 'hamsterkombat/config.json'))
    
from influxdb_client import InfluxDBClient, QueryApi
client = InfluxDBClient(url=read_json(config['influxdb_config_path'])['influxdb_url'], 
                        token=read_json(config['influxdb_config_path'])['influxdb_token'])
query_api = client.query_api()

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
    return jsonify(read_json(os.path.join(current_dir, 'hamster_config.json')))

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
    
@hamster.route('/api/graph_data')
def get_graph_data():
    graph_type = request.args.get('type', 'earnPassivePerHour')
    time_range = int(request.args.get('range', 86400))  # Default to 1 minute

    # Определяем интервал агрегации в зависимости от временного диапазона
    if time_range <= 86400:  # 1 день или меньше
        interval = '1h'
    elif time_range <= 604800:  # 7 дней или меньше
        interval = '6h'
    elif time_range <= 2592000:  # 1 месяц или меньше
        interval = '1d'
    else:
        interval = '1w'

    query = f"""
    from(bucket:"{config['influxdb_bucket']}")
    |> range(start: -{time_range}s)
    |> filter(fn: (r) => r._measurement == "measurement")
    |> filter(fn: (r) => r._field == "{graph_type}")
    |> aggregateWindow(every: {interval}, fn: mean, createEmpty: false)
    |> yield(name: "mean")
    """

    result = client.query_api().query(query, org=config['influxdb_org'])

    timestamps = []
    values = []
    fan_states = []

    for table in result:
        for record in table.records:
            timestamps.append(record.get_time().strftime('%Y-%m-%d %H:%M:%S'))
            if record.get_field() == graph_type:
                values.append(record.get_value())
            elif record.get_field() == 'fan_state':
                fan_states.append(round(record.get_value()))  # Округляем состояние вентилятора