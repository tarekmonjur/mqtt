
from flask import Blueprint, render_template
from db import db_connect, login_required

app_name = "Attendance Broker"
bp = "/dashboard"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route('/', methods=['GET'])
@login_required
def index():
    data = {
        "appName": app_name,
        "title": "Dashbaord"
    }
    db = db_connect()
    cursor = db.cursor()
    sql_query = "SELECT COUNT(id) AS total_device FROM devices"
    cursor.execute(sql_query)
    device = cursor.fetchone()
    data["total_device"] = device[0]

    sql_query = "SELECT COUNT(id) AS total_webhook FROM webhooks"
    cursor.execute(sql_query)
    webhook = cursor.fetchone()
    data["total_webhook"] = webhook[0]
    print(data)
    return render_template('index.html', data=data)
