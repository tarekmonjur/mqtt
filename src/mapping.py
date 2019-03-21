
from flask import Blueprint, request, render_template, flash, redirect, url_for
from datetime import datetime
from db import db_connect

app_name = "Broker & Webhook"
bp = "/mapping"
app = Blueprint(bp, __name__, url_prefix='/')


@app.route(bp+'/index', methods=['GET'])
def index():
    data = {
        "appName": app_name,
        "title": "Device Mapping"
    }
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql_query = "select devices.*, webhooks.school_name from devices join webhooks on devices.webhook_id = webhooks.id order by id desc"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        data['devices'] = result
        print(result)
    except:
        flash('Sorry! Something was wrong.', 'error')
    finally:
        cursor.close()
        db.close()
        return render_template('mapping/index.html', data=data)


@app.route(bp+'/add', methods=['GET'])
def add():
    data = {
        "appName": app_name,
        "title": "Device Mapping"
    }
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql_query = "select * from webhooks order by id desc"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        data['webhooks'] = result
    except:
        flash('Sorry! Something was wrong.', 'error')
    finally:
        cursor.close()
        db.close()
        return render_template('mapping/add.html', data=data)


@app.route(bp+'/add', methods=['POST'])
def store():
    try:
        input_data = request.form
        db = db_connect()
        cursor = db.cursor()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_query = "insert into devices (webhook_id, device_number, rf_id, channel, created_at) values (%s,%s,%s,%s,%s)"
        insert_data = (input_data['webhook_id'], input_data['device_number'], input_data['rf_id'], input_data['channel'], created_at)
        cursor.execute(sql_query, insert_data)
        db.commit()
        flash('School Device successfully mapped', 'success')
        return redirect(url_for('/mapping.index'))
    except:
        flash('Sorry! Device not mapped. Please try again.', 'error')
        return redirect(url_for('/mapping.add'))
    finally:
        cursor.close()
        db.close()




