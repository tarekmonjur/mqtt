
from flask import Blueprint, request, render_template

app_name = "Broker & Webhook"
bp = "/mapping"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route(bp+'/index', methods=['GET'])
def index():
    data = {
        "appName": app_name,
        "title": "Device Mapping"
    }
    return render_template('mapping/index.html', data=data)


@app.route(bp+'/add', methods=['GET'])
def add():
    data = {
        "appName": app_name,
        "title": "Device Mapping"
    }
    return render_template('mapping/add.html', data=data)

