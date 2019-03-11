
from flask import Blueprint, request, render_template
app = Blueprint('/dashboard', __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    data = {
        "appName": "Attendance WebHook",
        "title": "Dashbaord"
    }

    print(data)
    return render_template('index.html', data=data)
