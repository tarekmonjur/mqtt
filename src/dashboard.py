
from flask import Blueprint, request, render_template
app = Blueprint('/dashboard', __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    data = {"AppName": "WebHook"}
    print(data)
    return render_template('index.html', data=data)


@app.route('/webhook')
def webhook():
    data = {''}
    return render_template('index.html', data=data)

