import paho.mqtt.client as mqtt
from flask import Flask
import json
import time
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
apiUrl = 'http://school.attendance/api/v1/attendances'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #print("data " + str(userdata))
    #print("flags " + str(flags))
    #print("client " + str(client))
    client.subscribe("DBNSCHOOLRFID")


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    if message.topic == "DBNSCHOOLRFID":
        print(message.payload)

        messageData = message.payload.split(',')
        jsonPayload = {}
        jsonPayload['device_id'] = messageData[0]
        jsonPayload['rf_id'] = messageData[1]
        deviceId = messageData[0]

        # jsonPayload = json.loads(message.payload)
        # print(jsonPayload)

        # jsonPayload = json.loads('{"device_id": "00001", "rf_id": "'+message.payload+'"}')
        # print(jsonPayload['device_id'])
        # print(jsonPayload['rf_id'])
        # '{"device_id": "00001", "rf_id": "0012"}'

        headers = {"api-token": "U7rxIBBOoTcRdrdO4lsKoTb1Vtopxyb81549424252"}
        # print(headers)

        result = requests.post(apiUrl, params=jsonPayload, headers=headers)
        res = result.json()
        if res['code'] == 200 and res['status'] == "success":
            print(res['message'])
            client.publish(deviceId, '1')
        else:
            print(res['message'])
            client.publish(deviceId, '0')

        # print(res['status'])
        # print(res['code'])
        # print(res['title'])
        # print(res['message'])


mqttc = mqtt.Client()
mqttc.username_pw_set("tarek", password="tarek99")
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60, "localhost")
mqttc.loop_start()
# mqttc.loop_forever()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)