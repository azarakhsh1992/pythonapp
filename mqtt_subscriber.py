
import paho.mqtt.client as mqtt
import time
import datetime

previous_time1 = None  # Initialize previous_time variable
previous_time2 = None  # Initialize previous_time variable

topic1="/VW/Halle1/FactoryEdge1_SetVoltage"
topic2="iolink/process/port/2"
topic3="iolink/process/port/3"
topic4="iolink/process/port/4"
topic5="iolink/process/port/5"
topic6="iolink/process/port/6"
topic7="iolink/process/port/7"
topic8="iolink/process/port/8"
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to multiple topics
    
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)
    client.subscribe(topic5)
    client.subscribe(topic6)
    client.subscribe(topic7)
    client.subscribe(topic8)


def on_message(client, userdata, msg):
    global previous_time1 
    global previous_time2 
    if msg.topic == topic1:
        current_time1 = datetime.datetime.now().second
        print(f"current time Topic1: {current_time1}")
        if previous_time1 is not None:
            time_difference1 = current_time1 - previous_time1
            print(f"Time difference Topic1 : {time_difference1}")
        else:
            pass
        previous_time1 = current_time1
        print(f"Received message from {topic1}: {msg.payload.decode()}")        
    elif msg.topic == topic2:
        current_time2 = datetime.datetime.now().second
        print(f"current time Topic2: {current_time2}")
        if previous_time2 is not None:
            time_difference2 = current_time2 - previous_time2
            print(f"Time difference Topic2 : {time_difference2}")
        else:
            pass
        previous_time2 = current_time2
        print(f"Received message from {topic2}: {msg.payload.decode()}")        
    
    elif msg.topic == topic3:
            print(f"Received message from {topic3}: {msg.payload.decode()}")
    elif msg.topic == topic4:
            print(f"Received message from {topic4}: {msg.payload.decode()}")
    elif msg.topic == topic5:
            print(f"Received message from {topic5}: {msg.payload.decode()}")
    elif msg.topic == topic6:
            print(f"Received message from {topic6}: {msg.payload.decode()}")
    elif msg.topic == topic7:
            print(f"Received message from {topic7}: {msg.payload.decode()}")
    elif msg.topic == topic8:
            print(f"Received message from {topic8}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.1", 1883, 60)
client.loop_forever()
