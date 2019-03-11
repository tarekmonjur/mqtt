
from flask import Blueprint, request, render_template
bp = "/webhook"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route(bp+'/index', methods=['GET'])
def index():
    data = {
        "appName": "Attendance WebHook",
        "title": "Webhooks"
    }
    return render_template('webhook/index.html', data=data)


@app.route(bp+'/add', methods=['GET'])
def add():
    data = {
        "appName": "Attendance WebHook",
        "title": "Webhooks"
    }
    return render_template('webhook/add.html', data=data)


@app.route(bp+'/add', methods=['POST'])
def store():
    print(request.form)
    data = {
        "appName": "Attendance WebHook",
        "title": "Webhooks"
    }
    return render_template('webhook/add.html', data=data)