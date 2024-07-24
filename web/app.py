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

# Динамическая загрузка модулей
modules = []
for module_name, module_info in modules_paths.items():
    module = __import__(f"modules.{module_name}.route", fromlist=[''])
    blueprint = getattr(module, module_name)
    app.register_blueprint(blueprint, url_prefix=f'/{module_name}')
    

@app.route('/')
def index():
    return render_template('base_layout.html', modules=modules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)