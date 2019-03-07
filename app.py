import paho.mqtt.client as mqtt
import json
import time
import requests
from src import create_app

apiUrl = 'http://school.attendance/api/v1/attendances'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #print("data " + str(userdata))
    #print("flags " + str(flags))
    #print("client " + str(client))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SRFID")


# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))
    if message.topic == "SRFID":
        print("readings update data...")
        print(message.payload)
        # jsonPayload = json.loads(message.payload)
        jsonPayload = json.loads('{"device_id": "00001", "rf_id": "'+message.payload+'"}')
        # print(jsonPayload)
        # print(jsonPayload['device_id'])
        # print(jsonPayload['rf_id'])
        # '{"device_id": "00001", "rf_id": "0012"}'
        headers = {"api-token": "U7rxIBBOoTcRdrdO4lsKoTb1Vtopxyb81549424252"}
        # print(jsonPayload)
        # print(headers)
        result = requests.post(apiUrl, params=jsonPayload, headers=headers)
        res = result.json()
        if res['code'] == 200 and res['status'] == "success":
            print(res['message'])
        # print(res['status'])
        # print(res['code'])
        # print(res['title'])
        # print(res['message'])


# mqtt config
mqttc = mqtt.Client()
mqttc.username_pw_set("tarek", password="tarek99")
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60, "localhost")
mqttc.loop_start()
# mqttc.loop_forever()


if __name__ == "__main__":
    app = create_app()
