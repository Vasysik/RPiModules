from flask import Blueprint, render_template, jsonify, request
import json
import subprocess

store = Blueprint('store', __name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='static')

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

@store.route('/')
def index():
    return render_template('store.html')

@store.route('/api/available_modules')
def get_available_modules():
    available_modules = read_json('modules/store/available_modules.json')
    modules_paths = read_json('modules.json')
    installed_modules = set(modules_paths.keys())
    filtered_modules = [module for module in available_modules if module['name'] not in installed_modules]
    return jsonify(filtered_modules)

@store.route('/api/install_module', methods=['POST'])
def install_module():
    data = request.json
    repo_url = data.get('repo')
    module_name = data.get('name')
    
    if not repo_url or not module_name:
        return jsonify({"error": "Missing repository URL or module name"}), 400

    modules_paths = read_json('modules.json')
    if module_name in modules_paths:
        return jsonify({"error": "Module already installed"}), 400

    try:
        # Клонирование репозитория
        subprocess.run(['git', 'clone', repo_url, f'modules/{module_name}'], check=True)

        # Обновление modules.json
        modules_paths[module_name] = {
            "route": module_name,
            "icon": f"{module_name}/static/{module_name}_icon.png",
            "name": module_name,
            "enable": True
        }
        
        with open('modules.json', 'w') as f:
            json.dump(modules_paths, f, indent=4)

        return jsonify({"success": True, "message": f"Module {module_name} installed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500