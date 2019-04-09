
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
        sql_query = "select devices.*, webhooks.school_name from devices left join webhooks on devices.webhook_id = webhooks.id order by id desc"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        data['devices'] = result
        # print(result)
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
        sql_query = "insert into devices (webhook_id, device_number, created_at) values (%s,%s,%s)"
        insert_data = (input_data['webhook_id'], input_data['device_number'], created_at)
        cursor.execute(sql_query, insert_data)
        db.commit()
        flash('School Device successfully mapped', 'success')
        if input_data['submit'] == 'save':
            return redirect(url_for('/mapping.index'))
        else:
            return redirect(url_for('/mapping.add'))
    except:
        flash('Sorry! Device not mapped. Please try again.', 'error')
        return redirect(url_for('/mapping.add'))
    finally:
        cursor.close()
        db.close()


@app.route(bp+'/edit/<int:device_id>', methods=['GET'])
def edit(device_id):
    data = {
        "appName": app_name,
        "title": "Edit Mapping"
    }
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql_query = "SELECT * FROM devices WHERE id = %s"
        input_tuple = (device_id,)
        cursor.execute(sql_query, input_tuple)
        data['device'] = cursor.fetchone()

        sql_query = "select * from webhooks order by id desc"
        cursor.execute(sql_query)
        data['webhooks'] = cursor.fetchall()
    except:
        flash('Sorry! Something was wrong.', 'error')
    finally:
        cursor.close()
        db.close()
        return render_template('mapping/edit.html', data=data)


@app.route(bp+'/edit/<int:device_id>', methods=['POST'])
def update(device_id):
    try:
        input_data = request.form
        db = db_connect()
        cursor = db.cursor()
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_query = "UPDATE devices SET webhook_id=%s, device_number=%s, updated_at=%s WHERE id=%s"
        update_data = (input_data['webhook_id'], input_data['device_number'], updated_at, device_id)
        cursor.execute(sql_query, update_data)
        db.commit()
        flash('Device mapping successfully updated', 'success')
        return redirect(url_for('/mapping.index'))
    except:
        db.rollback()
        flash('Sorry! Device not mapped. Please try again.', 'error')
        return redirect(url_for('/mapping.edit', device_id = device_id))
    finally:
        cursor.close()
        db.close()


@app.route(bp + '/delete/<int:device_id>', methods=['GET'])
def delete(device_id):
    try:
        db = db_connect()
        cursor = db.cursor()
        sql_query = "DELETE FROM devices WHERE id=%s"
        delete_tuple = (device_id,)
        cursor.execute(sql_query, delete_tuple)
        db.commit()
        flash('Device mapping successfully deleted.', 'success')
    except:
        db.rollback()
        flash('Sorry! Device mapping not deleted.', 'error')
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('/mapping.index'))
