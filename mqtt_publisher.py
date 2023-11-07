import paho.mqtt.client as mqtt
import random
import time
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler


def publish_msg():
    this_topic ='PLC1'
    this_message ='PLC1latch_ACF:TRUE'
    broker='192.168.1.1'
    client = mqtt.Client()
    client.connect(broker,port=1883)
    client.publish(this_topic, this_message)
    client.loop_start()
    client.disconnect()
    time.sleep(3)
    this_message ='PLC1latch_ACF:FALSE'
    broker='192.168.1.1'
    client = mqtt.Client()
    client.connect(broker,port=1883)
    client.publish(this_topic, this_message)
    client.loop_start()
    client.disconnect()

publish_msg()