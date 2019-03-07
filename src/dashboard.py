
from flask import Blueprint, request, render_template
bp = Blueprint('/dashboard', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/home')
def home():
    return 'home page'

