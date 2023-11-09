
import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests


def delayed_publish(client,PLC_name, module_topic):
        time.sleep(3)
        this_topic = PLC_name
        this_message = module_topic+':close'
        client.publish(this_topic, this_message)


def send_temperature(msg):
    if msg.topic in [Topic_LDH_edgeA1,Topic_LDH_edgeA2,Topic_LDH_edgeA3,Topic_LDH_edgeB1,Topic_LDH_edgeB2,\
                    Topic_LDH_edgeB3,Topic_LDH_energy,Topic_LDH_network]:    
        for msg.topic in [Topic_LDH_edgeA1,Topic_LDH_edgeA2,Topic_LDH_edgeA3,Topic_LDH_edgeB1,Topic_LDH_edgeB2,\
                        Topic_LDH_edgeB3,Topic_LDH_energy,Topic_LDH_network]:
            payload = {}
            payload.append(json_convert_temp(msg))
            send_to_django_server(payload)


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
    

PLC_name = "PLC1"
broker = '192.168.1.1'
url='http://127.0.0.1:8000/temp_sensors_msg/'


Topic_LDH_edgeA1=PLC_name+"LDH_edgeA1"
Topic_LDH_edgeA2=PLC_name+"LDH_edgeA2"
Topic_LDH_edgeA3=PLC_name+"LDH_edgeA3"
Topic_LDH_edgeB1=PLC_name+"LDH_edgeB1"
Topic_LDH_edgeB2=PLC_name+"LDH_edgeB2"
Topic_LDH_edgeB3=PLC_name+"LDH_edgeB3"
Topic_LDH_network=PLC_name+"LDH_network"
Topic_LDH_energy=PLC_name+"LDH_energy"

Topic_EM1=PLC_name+"EM1"
Topic_EM2=PLC_name+"EM2"


Topic1=PLC_name+"door_sensor_edgeAF"
Topic2=PLC_name+"door_sensor_edgeAB"
Topic3=PLC_name+"door_sensor_edgeBF"
Topic4=PLC_name+"door_sensor_edgeBB"
Topic5=PLC_name+"door_sensor_network"
Topic6=PLC_name+"door_sensor_energy"
Topic7=PLC_name+"door_sensor_ACF"
Topic8=PLC_name+"door_sensor_ACB"

Topic9=PLC_name+"latch_sensor_edgeAF"	
Topic10=PLC_name+"latch_sensor_edgeAB"	
Topic11=PLC_name+"latch_sensor_edgeBF"	
Topic12=PLC_name+"latch_sensor_edgeBB"	
Topic13=PLC_name+"latch_sensor_network"	
Topic14=PLC_name+"latch_sensor_energy"	
Topic15=PLC_name+"latch_sensor_ACF"	
Topic16=PLC_name+"latch_sensor_ACB"	

Topic17=PLC_name+"latch_edge_AF"
Topic18=PLC_name+"latch_edge_AB"
Topic19=PLC_name+"latch_edge_BF"
Topic20=PLC_name+"latch_edge_BB"
Topic21=PLC_name+"latch_network"
Topic22=PLC_name+"latch_energy"
Topic23=PLC_name+"latch_ACF"
Topic24=PLC_name+"latch_ACB"

Topic25=PLC_name+"LED_1_edgeAF"
Topic26=PLC_name+"LED_2_edgeAF"
Topic27=PLC_name+"LED_3_edgeAF"
Topic28=PLC_name+"LED_4_edgeAF"

Topic29=PLC_name+"LED_1_edgeAB"
Topic30=PLC_name+"LED_2_edgeAB"
Topic31=PLC_name+"LED_3_edgeAB"
Topic32=PLC_name+"LED_4_edgeAB"

Topic33=PLC_name+"LED_1_edgeBF"
Topic34=PLC_name+"LED_2_edgeBF"
Topic35=PLC_name+"LED_3_edgeBF"
Topic36=PLC_name+"LED_4_edgeBF"

Topic37=PLC_name+"LED_1_edgeBB"
Topic38=PLC_name+"LED_2_edgeBB"
Topic39=PLC_name+"LED_3_edgeBB"
Topic40=PLC_name+"LED_4_edgeBB"

Topic41=PLC_name+"LED_1_network"
Topic42=PLC_name+"LED_2_network"
Topic43=PLC_name+"LED_3_network"
Topic44=PLC_name+"LED_4_network"

Topic45=PLC_name+"LED_1_energy"
Topic46=PLC_name+"LED_2_energy"
Topic47=PLC_name+"LED_3_energy"
Topic48=PLC_name+"LED_4_energy"

Topic49=PLC_name+"LED_1_ACF"
Topic50=PLC_name+"LED_2_ACF"
Topic51=PLC_name+"LED_3_ACF"
Topic52=PLC_name+"LED_4_ACF"

Topic53=PLC_name+"LED_1_ACB"
Topic54=PLC_name+"LED_2_ACB"
Topic55=PLC_name+"LED_3_ACB"
Topic56=PLC_name+"LED_4_ACB"

Topic57=PLC_name+"AC_sensor1"
Topic58=PLC_name+"AC_sensor2"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to multiple Topics

    client.subscribe(Topic_LDH_edgeA1)
    client.subscribe(Topic_LDH_edgeA2)
    client.subscribe(Topic_LDH_edgeA3)
    client.subscribe(Topic_LDH_edgeB1)
    client.subscribe(Topic_LDH_edgeB2)
    client.subscribe(Topic_LDH_edgeB3)
    client.subscribe(Topic_LDH_network)
    client.subscribe(Topic_LDH_energy)


    client.subscribe(Topic_EM1)
    client.subscribe(Topic_EM2)


    client.subscribe(Topic1)
    client.subscribe(Topic2)
    client.subscribe(Topic3)
    client.subscribe(Topic4)
    client.subscribe(Topic5)
    client.subscribe(Topic6)
    client.subscribe(Topic7)
    client.subscribe(Topic8)
    client.subscribe(Topic9)
    client.subscribe(Topic10)
    client.subscribe(Topic11)
    client.subscribe(Topic12)
    client.subscribe(Topic13)
    client.subscribe(Topic14)
    client.subscribe(Topic15)
    client.subscribe(Topic16)
    client.subscribe(Topic17)
    client.subscribe(Topic18)
    client.subscribe(Topic19)
    client.subscribe(Topic20)
    client.subscribe(Topic21)
    client.subscribe(Topic22)
    client.subscribe(Topic23)
    client.subscribe(Topic24)
    client.subscribe(Topic25)
    client.subscribe(Topic26)
    client.subscribe(Topic27)
    client.subscribe(Topic28)
    client.subscribe(Topic29)
    client.subscribe(Topic30)
    client.subscribe(Topic31)
    client.subscribe(Topic32)
    client.subscribe(Topic33)
    client.subscribe(Topic34)
    client.subscribe(Topic35)
    client.subscribe(Topic36)
    client.subscribe(Topic37)
    client.subscribe(Topic38)
    client.subscribe(Topic39)
    client.subscribe(Topic40)
    client.subscribe(Topic41)
    client.subscribe(Topic42)
    client.subscribe(Topic43)
    client.subscribe(Topic44)
    client.subscribe(Topic45)
    client.subscribe(Topic46)
    client.subscribe(Topic47)
    client.subscribe(Topic48)
    client.subscribe(Topic49)
    client.subscribe(Topic50)
    client.subscribe(Topic51)
    client.subscribe(Topic52)
    client.subscribe(Topic53)
    client.subscribe(Topic54)
    client.subscribe(Topic55)
    client.subscribe(Topic56)
    client.subscribe(Topic57)
    client.subscribe(Topic58)



def on_message(client, userdata, msg):

    if msg.topic == Topic1:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic1)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic2:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic2)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic3:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic3)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic4:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic4)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic5:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic5)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic6:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic6)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic7:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic7)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic8:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic8)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic9:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic9)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic10:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic10)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic11:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic11)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic12:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic12)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic13:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic13)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic14:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic14)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic15:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic15)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic16:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic16)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic17:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic17)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic18:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic18)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic19:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic19)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic20:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic20)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic21:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic21)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic22:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic22)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic23:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic23)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic24:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic24)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic25:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic25)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic26:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic26)).start()
        send_to_django_server(payload)

    elif msg.topic == Topic27:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic27)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic28:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic28)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic29:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic29)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic30:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic30)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic31:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic31)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic32:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic32)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic33:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic33)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic34:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic34)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic35:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic35)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic36:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic36)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic37:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic37)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic38:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic38)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic39:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic39)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic40:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic40)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic45:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic45)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic46:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic46)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic47:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic47)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic48:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic48)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic49:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic49)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic50:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic50)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic51:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic51)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic52:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic52)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic53:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic53)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic54:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic54)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic55:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic55)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic56:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic56)).start()
        send_to_django_server(payload)
        
    elif msg.topic == Topic57:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic57)).start()
        send_to_django_server(payload)


    elif msg.topic == Topic58:
        payload=json_convert_dido(msg)
        if payload.get('value') == "open":  # Assuming the value is a boolean True
            threading.Thread(target=delayed_publish, args=(client, Topic58)).start()
        send_to_django_server(payload)




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.1", 1883, 60)
client.loop_forever()