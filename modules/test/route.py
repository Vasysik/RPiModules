from flask import Blueprint, render_template
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
fan_control = Blueprint('test', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='static')

@fan_control.route('/')
def index():
    return render_template('test.html')