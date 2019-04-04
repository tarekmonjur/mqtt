
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
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql_query = "select * from webhooks order by id desc"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        data['results'] = result
        # print(data)
    except:
        flash('Sorry! Something was wrong.', 'error')
    finally:
        cursor.close()
        db.close()
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
        flash('School webhook successfully added.', 'success')
        return redirect(url_for('/webhook.index'))
    except:
        flash('Sorry! School webhook not added. Please try again.', 'error')
        return redirect(url_for('/webhook.add'))
    finally:
        cursor.close()
        db.close()


@app.route(bp+'/edit/<int:webhook_id>', methods=['GET'])
def edit(webhook_id):
    data = {
        "appName": app_name,
        "title": "Edit Webhook"
    }
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql_query = "SELECT * FROM webhooks WHERE id = %s"
        input_tuple = (webhook_id,)
        cursor.execute(sql_query, input_tuple)
        result = cursor.fetchone()
        data['webhook'] = result
    except:
        flash('Sorry! Something was wrong.', 'error')
    finally:
        cursor.close()
        db.close()
        return render_template('webhook/edit.html', data=data)


@app.route(bp+'/update/<int:webhook_id>', methods=['POST'])
def update(webhook_id):
    input_data = request.form
    try:
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = db_connect()
        cursor = db.cursor()
        sql_query = "UPDATE webhooks SET school_name=%s, school_domain=%s, api_token=%s, api_url=%s, updated_at=%s WHERE id=%s"
        update_tuple = (input_data['school_name'], input_data['school_domain'], input_data['api_token'], input_data['api_url'], updated_at, webhook_id)
        # print(insert_tuple)
        cursor.execute(sql_query, update_tuple)
        db.commit()
        flash('School webhook successfully updated.', 'success')
        return redirect(url_for('/webhook.index'))
    except:
        flash('Sorry! School webhook not updated. Please try again.', 'error')
        return redirect(url_for('/webhook.edit'))
    finally:
        cursor.close()
        db.close()


@app.route(bp+'/delete/<int:webhook_id>', methods=['GET'])
def delete(webhook_id):
    try:
        db = db_connect()
        cursor = db.cursor()
        sql_query = "DELETE FROM webhooks WHERE id = %s"
        delete_tuple = (webhook_id,)
        cursor.execute(sql_query, delete_tuple)
        db.commit()
        flash('School webhook successfully deleted.', 'success')
    except:
        flash('Sorry! School webhook not deleted.', 'error')
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('/webhook.index'))

