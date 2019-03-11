
from flask import Blueprint, request, render_template

app_name = "Attendance Broker"
bp = "/dashboard"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    data = {
        "appName": app_name,
        "title": "Dashbaord"
    }

    print(data)
    return render_template('index.html', data=data)
