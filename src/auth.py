
from flask import Blueprint, request, render_template, sessions, flash, redirect, url_for
from db import db_connect

app_name = "Attendance Broker"
bp = "/auth"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route('/login', methods=['GET', 'POST'])
def index():
    data = {
        "appName": app_name,
        "title": "Log In Page"
    }
    if request.method == 'POST':
        print(request.form)
        email = request.form["email"]
        passowrd = request.form["password"]
        sql = "select * from users where email=%s"
        user = (email,)
        db = db_connect()
        cursor = db.cursor()
        cursor.execute(sql, user)
        result = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        print(result[2])

    return render_template('login.html', data=data)


@app.route('/logout', methods=['GET'])
def logout():
    print('logout')