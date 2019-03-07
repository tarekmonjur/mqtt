
from flask import Blueprint, request, render_template
bp = Blueprint('/auth', __name__, url_prefix='/')

@bp.route('/login')
def index():
    return render_template('login.html', appName='DBN')