from flask import Blueprint, render_template, request, jsonify
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
fan_control = Blueprint('fan_control', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='static')

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

config = read_json(os.path.join(current_dir, 'config.json'))
settings = read_json(os.path.join(current_dir, 'settings.json'))

from influxdb_client import InfluxDBClient, QueryApi
client = InfluxDBClient(url=read_json(config['influxdb_config_path'])['influxdb_url'], 
                        token=read_json(config['influxdb_config_path'])['influxdb_token'])
query_api = client.query_api()

@fan_control.route('/')
def index():
    influxdb_bucket = config['influxdb_bucket']
    influxdb_org = config['influxdb_org']
    
    query = f'from(bucket: "{influxdb_bucket}") |> range(start: -5m) |> filter(fn: (r) => r._measurement == "fan_status") |> last()'
    result = query_api.query(org=influxdb_org, query=query)
    return render_template('fan_control.html')

@fan_control.route('/api/current', methods=['GET'])
def api_current():
    influxdb_bucket = config['influxdb_bucket']
    influxdb_org = config['influxdb_org']

    query = f'from(bucket: "{influxdb_bucket}") |> range(start: -5m) |> filter(fn: (r) => r._measurement == "fan_status") |> last()'
    result = query_api.query(org=influxdb_org, query=query)
    current_data = {}
    if result:
        for table in result:
            record = table.records[0]
            field_name = record.get_field()
            if field_name == 'temperature':
                current_data["Temperature"] = record.get_value()
            elif field_name == 'fan_state':
                current_data["Fan_State"] = record.get_value()
    return jsonify(current_data)

@fan_control.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    if request.method == 'GET':
        return jsonify(settings)
    elif request.method == 'POST':
        data = request.json
        write_json(os.path.join(current_dir, 'settings.json'), data)
        return jsonify({"status": "success"}), 200
