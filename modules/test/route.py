from flask import Blueprint, render_template
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
test = Blueprint('test', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='static')

@test.route('/')
def index():
    return render_template('test.html')