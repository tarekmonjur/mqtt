
from flask import Blueprint, request, render_template
bp = "/mapping"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route(bp+'/index', methods=['GET'])
def index():
    data = {
        "appName": "Attendance WebHook",
        "title": "Device Mapping"
    }
    return render_template('mapping/index.html', data=data)

