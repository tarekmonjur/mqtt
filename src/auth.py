
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
import hashlib
from db import db_connect, guest_required, login_required

app_name = "Broker & Webhook"
bp = "/auth"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route('/login', methods=['GET', 'POST'])
@guest_required
def index():
    data = {
        "appName": app_name,
        "title": "Log In Page"
    }
    if request.method == 'POST':
        try:
            email = request.form["email"]
            password = request.form["password"]
            password = hashlib.sha256(password).hexdigest()
            db = db_connect()
            cursor = db.cursor(dictionary=True)
            sql_query = "select * from users where email=%s and password=%s"
            query_tuple = (email,password)
            cursor.execute(sql_query, query_tuple)
            result = cursor.fetchone()
            db.commit()
            if result is not None and result:
                session.clear()
                session['auth'] = result
                print(session['auth'])
                session["login"] = True
                return redirect(url_for('/dashboard.index'))
            else:
                flash('Sorry! Username/Password was wrong.', 'error')
                return render_template('login.html', data=data)
        except:
            db.rollback()
        finally:
            cursor.close()
            db.close()
    else:
        return render_template('login.html', data=data)


@app.route('/gen-pass/<password>', methods=['GET'])
def password_generate(password):
    return hashlib.sha256(password).hexdigest() +'-------------'+ hashlib.sha256(password).hexdigest()


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('/auth.index'))

