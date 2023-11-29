
import paho.mqtt.client as mqtt
import time, datetime
import threading


import requests
##############################################################
Topic = "test"
broker = '192.168.1.1'
def send_to_django_server(payload):
    # Define the URL of your Django server endpoint
    url = 'http://127.0.0.1:8000/web/MqttMiddleware/dido/'
    headers = {'Content-Type': 'application/json'}
    print(payload)
    if payload != "F":
        try:
            response = requests.post(url, json=payload, headers=headers,)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}", e.response.text)
            
    else:
        pass
    
def on_connect(client, userdata, flags, rc):
    print(f"Main Thread: Connected with result code {rc}")

    client.subscribe(Topic)
    
def on_message(client, userdata, msg):
    
    if msg.topic == Topic:
        current_time=time.time()
        print(current_time)
        
        payload={'profinet_name':'BBBBBsBBBBB','value':True,'F':'False','time':current_time}
    threading.Thread(target=send_to_django_server, args=(payload,)).start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()