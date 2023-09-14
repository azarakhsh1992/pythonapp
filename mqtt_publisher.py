import paho.mqtt.client as mqtt
import random
import time
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler



def on_connect(client, userdata, flags, rc, this_topic, this_payload):
    print(f"Connected with result code {rc}")
    client.publish(topic =this_topic, payload = this_payload, qos = 0, retain = True)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.1", 1883, 60)
client.loop_forever()

