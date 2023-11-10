
import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests
import re
from functions import *


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_complex_to_json(data_string):
    # Replace 'time' with a string value and boolean values with lowercase
    data_string = data_string.replace('time', '"time"').replace('FALSE', 'False').replace('TRUE', 'True')
    
    # Insert quotes around keys and process values
    new_pairs = []
    for pair in data_string.strip('{}').split(','):
        key, value = pair.split(":")

        # Check if the value is a float
        if is_float(value):
            value = float(value)  # Cast to float
        # Check for boolean values
        elif value.lower() in ['true', 'false']:
            value = value.lower()
        else:
            # For other non-numeric, non-boolean values, keep them as strings
            value = f'"{value}"'

        # If the key is one of the specified ones, make sure the value is a float
        if key in ['T', 'Tmin', 'Tmax', 'RH']:
            value = float(value)

        new_pair = f'"{key}":{value}'
        new_pairs.append(new_pair)

    data_string = ','.join(new_pairs)

    # Convert to JSON object
    json_object = json.loads(f'{{{data_string}}}')
    
    return json.dumps(json_object, indent=2)

def convert_simple_to_json(data_string):
    # Replace boolean values with lowercase
    data_string = data_string.replace('FALSE', 'False').replace('TRUE', 'True')
    
    # Insert quotes around keys and string values
    data_string = ','.join([f'"{pair.split(":")[0]}":"{pair.split(":")[1]}"' if not pair.split(":")[1].isdigit() else f'"{pair.split(":")[0]}":{pair.split(":")[1]}' for pair in data_string.strip('{}').split(',')])
    
    # Convert to JSON object
    json_object = json.loads(f'{{{data_string}}}')
    
    return json.dumps(json_object, indent=2)


PLC_name = "PLC1"
broker = '192.168.1.1'
url='http://127.0.0.1:8000/temp_sensors_msg/'



Topic23=PLC_name+"latch_ACF"
topic22=PLC_name+"LDH292"

def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to multiple Topics

        client.subscribe(Topic23)
        client.subscribe(topic22)
        
def on_message(client, userdata, msg):
    print(msg.payload.decode())
    if msg.topic == topic22:
        try:
            json_string=convert_complex_to_json(msg.payload.decode())
            payload_dict = json.loads(json_string)
            print(payload_dict)
            print(f"Received message from {topic22}:{payload_dict}")
            threading.Thread(target=delayed_publish, args=(client, Topic23)).start()
            send_to_django_server(payload_dict)  # Call the function to send data to Django
        except json.JSONDecodeError:
            print("Error decoding payload")

    if msg.topic == Topic23:
        try:
            json_string=convert_simple_to_json(msg.payload.decode())
            payload_dict = json.loads(json_string)
            print(json_string)
            print(payload_dict)
            #print(f"Received message from {Topic23}:{payload_dict}")
            if payload_dict.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic23)).start()
                send_to_django_server(payload_dict)  # Call the function to send data to Django
        except json.JSONDecodeError:
            print("Error decoding payload")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.1", 1883, 60)
client.loop_forever()


"T;25.5;Tmin;15;Tmax;30.644;RH;37;F;FALSE;Time;10y2d20h10s25ms"



    # if msg.topic == Topic1:
    #     payload=json_convert_dido(msg)
    #     if payload !="F":
    #         if payload.get('value') == "open":  # Assuming the value is a boolean True
    #             delayed_publish(client,Topic1)
    #         threading.Thread(target=send_to_django_server, args=(payload,)).start()
    #     else:
    #         print("fault")
    #         pass




    # elif msg.topic == Topic2:
    #     payload=json_convert_dido(msg)
    #     if payload !="F":
    #         if payload.get('value') == "open":  # Assuming the value is a boolean True
    #             threading.Thread(target=delayed_publish, args=(client, Topic2)).start()
    #         threading.Thread(target=send_to_django_server, args=(payload,)).start()
    #     else:
    #         print("fault")
    #         pass

