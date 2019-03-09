
from flask import Blueprint, request, render_template, sessions, flash, redirect, url_for
app = Blueprint('/auth', __name__, url_prefix='/')


@app.route('/login', methods=['GET', 'POST'])
def index():
    # print(request.form)
    # if request.method == 'GET':
    data = {"appName": 'DBN'}
    return render_template('login.html', data=data)


@app.route('/logout', methods=['GET'])
def logout():
    print('logout')