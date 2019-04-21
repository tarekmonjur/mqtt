import paho.mqtt.client as mqtt
import json
import time
import requests
from db import db_connect


def get_webhook(device_id, channel):
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql = "select * from attendance_webhook.webhooks as w join attendance_webhook.devices as d on d.webhook_id=w.id where d.device_number=%s and d.device_channel=%s"
        cursor.execute(sql, (device_id, channel))
        result = cursor.fetchone()
        return result
    except:
        print("db problem")
    finally:
        cursor.close()
        db.close()


def get_webhook_by_device(device_id):
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql = "select * from attendance_webhook.webhooks as w join attendance_webhook.devices as d on d.webhook_id=w.id where d.device_number=%s"
        cursor.execute(sql, (device_id,))
        result = cursor.fetchone()
        return result
    except:
        print("db problem")
    finally:
        cursor.close()
        db.close()


def get_channel():
    try:
        db = db_connect()
        cursor = db.cursor(dictionary=True)
        sql = "select device_channel from devices group by device_channel"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        print("db problem")
    finally:
        cursor.close()
        db.close()


def handle_request(client, deviceId, webhook, jsonPayload):
    print(jsonPayload)
    headers = {"api-token": webhook['api_token']}
    result = requests.post(webhook['api_url'], params=jsonPayload, headers=headers)
    res = result.json()
    if res['code'] == 200 and res['status'] == "success":
        print(res['message'])
        client.publish(deviceId, '1')
    else:
        print(res['message'])
        client.publish(deviceId, '0')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #print("data " + str(userdata))
    #print("flags " + str(flags))
    #print("client " + str(client))
    client.subscribe('SRFID')
    channels = get_channel()
    # print(channels)
    if channels is not None and len(channels) > 0:
        for channel in channels:
            client.unsubscribe(channel['device_channel'])
            client.subscribe(channel['device_channel'])
            print(channel['device_channel'])


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))
    # #print("data " + str(userdata))
    # #print("flags " + str(flags))
    # #print("client " + str(client))
    # client.unsubscribe('SRFID')
    # channels = get_channel()
    # # print(channels)
    # if channels is not None and len(channels) > 0:
    #     for channel in channels:
    #         client.unsubscribe(channel['device_channel'])
    #         print('dd')


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    messageData = message.payload.split(',')
    jsonPayload = {}
    jsonPayload['device_id'] = messageData[0]
    jsonPayload['rf_id'] = messageData[1]
    deviceId = messageData[0]

    if message.topic == "SRFID":
        webhook = get_webhook_by_device(deviceId)
        if webhook:
            print(webhook)
            handle_request(client, deviceId, webhook, jsonPayload)
    else:
        webhook = get_webhook(deviceId, message.topic)
        if webhook:
            print(webhook)
            handle_request(client, deviceId, webhook, jsonPayload)

    # messageData = message.payload.split(',')
    # jsonPayload = {}
    # jsonPayload['device_id'] = messageData[0]
    # jsonPayload['rf_id'] = messageData[1]
    # deviceId = messageData[0]

    # jsonPayload = json.loads(message.payload)
    # print(jsonPayload)

    # jsonPayload = json.loads('{"device_id": "00001", "rf_id": "'+message.payload+'"}')
    # print(jsonPayload['device_id'])
    # print(jsonPayload['rf_id'])
    # '{"device_id": "00001", "rf_id": "0012"}'

    # headers = {"api-token": "U7rxIBBOoTcRdrdO4lsKoTb1Vtopxyb81549424252"}
    # # print(headers)
    #
    # result = requests.post(apiUrl, params=jsonPayload, headers=headers)
    # res = result.json()
    # if res['code'] == 200 and res['status'] == "success":
    #     print(res['message'])
    #     client.publish(deviceId, '1')
    # else:
    #     print(res['message'])
    #     client.publish(deviceId, '0')

    # print(res['status'])
    # print(res['code'])
    # print(res['title'])
    # print(res['message'])


def mqtt_connection(flag=0):
    if flag == 0:
        mqttc = mqtt.Client(client_id="", clean_session=True)
        mqttc.username_pw_set("tarek", password="tarek99")
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.connect("localhost", 1883, 60, "localhost")
        mqttc.loop_start()
        # mqttc.loop_forever()
        print("flag 0")
    elif flag == 1:
        mqttc = mqtt.Client(client_id="", clean_session=True)
        mqttc.username_pw_set("tarek", password="tarek99")
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        # mqttc.on_disconnect = on_disconnect
        mqttc.disconnect()
        # mqttc.loop_stop()
        mqttc.connect("localhost", 1883, 60, "localhost")
        mqttc.reconnect()
        # mqttc.loop_start()
        print("flag 1")