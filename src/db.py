import mysql.connector
from mysql.connector import Error
from flask import session, redirect, url_for, g
from functools import wraps


def db_connect():
    try:
        conn = mysql.connector.connect(host='localhost',database='attendance_webhook',user='root',password='root')
        if conn.is_connected():
            print('Connected to MySQL database.')
            return conn
        else:
            print('DB not Connected.')

    except Error as e:
        print(e.message)
    #
    # finally:
    #     conn.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'login' not in session:
            return redirect(url_for('/auth.index'))
        else:
            g.auth = session.get("auth")
        return view(**kwargs)
    return wrapped_view


def guest_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'login' in session:
            return redirect(url_for('/dashboard.index'))
        return view(**kwargs)
    return wrapped_view



if __name__ == '__main__':
    db_connect()
