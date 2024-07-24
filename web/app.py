from flask import Flask, jsonify, redirect
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

modules_paths = read_json(os.path.join(current_dir, "modules.json"))

# Динамическая загрузка модулей
modules = []
for module_name, module_info in modules_paths.items():
    if module_info['enable']:
        module = __import__(f"modules.{module_name}.route", fromlist=[''])
        blueprint = getattr(module, module_name)
        name = module_info['name']
        route = module_info['route']
        icon = module_info['icon']
        app.register_blueprint(blueprint, url_prefix=f'/{module_info['route']}')
        modules.append({
            'name': f'{name}',
            'route': f'{route}',
            'icon': f'{icon}',
            'static': f'{route}/static/'
        })

@app.route('/')
def index():
    if modules:
        first_module_route = modules[0]['route']
        return redirect(f'/{first_module_route}')
    else:
        return "No modules available", 404

@app.route('/api/modules')
def api_modules():
    return jsonify(modules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)