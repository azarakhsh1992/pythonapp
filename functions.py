import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests
import re


def delayed_publish(client,PLC_name, module_topic):
        time.sleep(3)
        this_topic = PLC_name
        this_message = module_topic+':close'
        client.publish(this_topic, this_message)



def send_to_django_server(payload):
    # Define the URL of your Django server endpoint
    url = 'http://127.0.0.1:8000/temp_sensors_msg/'
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        # Handle successful request
        print(f"Data sent to Django server with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle exceptions for the HTTP request here
        print(f"Failed to send data to Django server: {e}")

def json_convert_temp(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE','"True"').replace('FALSE',"False").split(";")
        payload = {"profinet_name":msg.topic,"T": mstr[1],"Tmin": mstr[3],"Tmax": mstr[5],"RH": mstr[7],"F": mstr[9],"Time": mstr[11]},
        return payload
    except json.JSONDecodeError:
        raise Exception("Error decoding payload")

def json_convert_dido(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE',"True").replace('FALSE',"False").split(";")
        payload = {"profinet_name":msg.topic,"value": mstr[1], "F": mstr[3]}
        return payload
    except json.JSONDecodeError:
        raise Exception("Error decoding payload")


def json_convert_energy(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE','"True"').replace('FALSE',"False").split(";")
        payload = {"profinet_name":msg.topic,"E": mstr[1],"UnitE": mstr[3],"P": mstr[5],"UnitP": mstr[7],"F": mstr[9],"Time": mstr[11]},
        return payload
    except json.JSONDecodeError:
        raise Exception("Error decoding payload")