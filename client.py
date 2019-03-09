import paho.mqtt.client as mqtt
from flask import Flask

app = Flask(__name__)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("status")


# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))



# mqtt config
mqttc = mqtt.Client()
mqttc.username_pw_set("tarek", password="tarek99")
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60, "localhost")
mqttc.publish("DBNSCHOOLRFID", '0015')
mqttc.loop_start()
# mqttc.loop_forever()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
    app.run(threaded=True)
