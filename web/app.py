from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from influxdb_client import InfluxDBClient, Point, QueryApi

app = Flask(__name__)

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

modules = read_json("modules_paths.json")
influxdb_config = read_json("influxdb_config.json")

client = InfluxDBClient(url=influxdb_config['influxdb_url'], token=influxdb_config['influxdb_token'])
query_api = client.query_api()

@app.route(f'/fan_control')
def fan_control():
    module = modules['fan_control']
    path = module['path']
    settings = read_json(path+module['settings'])
    config = read_json(path+module['config'])
    influxdb_bucket = config['influxdb_bucket']
    influxdb_org = config['influxdb_org']
    
    query = f'from(bucket: "{influxdb_bucket}") |> range(start: -5m) |> filter(fn: (r) => r._measurement == "fan_status") |> last()'
    result = query_api.query(org=influxdb_org, query=query)
    current_data = {}
    if result:
        record = result[0].records[0]
        current_data = {
            "Temperature": record.values.get("temperature"),
            "Fan State": record.values.get("fan_state")
        }
    return render_template('fan_control.html', current=current_data)

@app.route('/fan_control/api/current', methods=['GET'])
def api_current():
    module = modules['fan_control']
    path = module['path']
    config = read_json(path+module['config'])
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
                current_data["Fan State"] = record.get_value()
    return jsonify(current_data)

@app.route('/fan_control/api/settings', methods=['GET', 'POST'])
def api_settings():
    module = modules['fan_control']
    path = module['path']
    settings = read_json(path+module['settings'])

    if request.method == 'GET':
        return jsonify(settings)
    elif request.method == 'POST':
        data = request.json
        write_json(path+module['settings'], data)
        return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
