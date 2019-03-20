
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from db import db_connect

app_name = "Broker & Webhook"
bp = "/webhook"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route(bp+'/index', methods=['GET'])
def index():
    data = {
        "appName": app_name,
        "title": "Webhooks"
    }
    db = db_connect()
    cursor = db.cursor(dictionary=True)
    sql_query = "select * from webhooks"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    data['results'] = result
    # print(data)
    return render_template('webhook/index.html', data=data)


@app.route(bp+'/add', methods=['GET'])
def add():
    data = {
        "appName": app_name,
        "title": "Add Webhook"
    }
    return render_template('webhook/add.html', data=data)


@app.route(bp+'/add', methods=['POST'])
def store():
    input_data = request.form
    try:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = db_connect()
        cursor = db.cursor()
        sql_query = "INSERT INTO webhooks (school_name,school_domain,api_token,api_url,created_at) values (%s,%s,%s,%s,%s)"
        insert_tuple = (input_data['school_name'], input_data['school_domain'], input_data['api_token'], input_data['api_url'], created_at)
        # print(insert_tuple)
        cursor.execute(sql_query, insert_tuple)
        db.commit()
        flash('School Webhook successfully added.', 'success')
        return redirect(url_for('/webhook.index'))
    except:
        # print("Failed inserting date object into MySQL table {}")
        flash('Sorry! School Webhook not added. Please try again.', 'error')
        return redirect(url_for('/webhook.add'))
    finally:
        db.close()
        cursor.close()
