
import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests
import os
import certifi

# PLC_name = "KAAASDASASDVDASDASACAD"
PLC_name = "CABA01XFST01F01---KFU1"
pre_profinet_name = PLC_name[:-7]
broker = '192.168.137.1'
django_url = 'https://localhost:5000/web/mqttmiddleware/'


cert_file_path = 'cert.pem'
key_file_path = 'key.pem'

#######################################################
##############################################################
def send_to_django_server_dido(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'dido/'
    headers = {'Content-type': 'application/json'}
    print("here")
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers,verify=False)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}")
            
    else:
        pass
    ##############################################################
def send_to_django_server_temp(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'temp/'
    headers = {'Content-Type': 'application/json'}
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers,verify=False)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}")
    else:
        pass
    ##############################################################
def send_to_django_server_energy(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'energy/'
    headers = {'Content-Type': 'application/json'}
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers,verify=False)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}")
    else:
        pass
#################################################################################
# received string from PLC: "T;25;Tmin;15.5;Tmax;32.4;RH;56.5;V;FALSE;Time;65468451sacc"
def json_convert_temp(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE',"True").replace('FALSE',"False").split(";")
        print(len(mstr))
        if len(mstr) == 12:
            try:
                current_time = str(datetime.datetime.now())
                # payload = {"profinet_name":msg.topic,"T": float(mstr[1]),"Tmin": float(mstr[3]),"Tmax": float(mstr[5]),"RH": float(mstr[7]),"validity": mstr[9],"Time": current_time}
                payload = {"profinet_name":msg.topic,"T": float(mstr[1]),"Tmin": float(mstr[3]),"Tmax": float(mstr[5]),"RH": float(mstr[7]),"validity": mstr[9],"Time": mstr[11]}
                print(payload)
                return payload
            except :
                return "F"
        else:
            print("length of string does not match")
            return "F"
    except json.JSONDecodeError or TypeError or IndexError or ValueError or KeyError or TabError or OverflowError or SyntaxError:
        return "F"
#################################################################################
# received string from PLC:   "E;1500;UnitE;KWh;P;15.5;UnitP;KW;V;TRUE;Time;value"
def json_convert_energy(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE','True').replace('FALSE',"False").split(";")
        if len(mstr) == 12:
            try:
                current_time = str(datetime.datetime.now())
                # payload = {"profinet_name":msg.topic,"E": float(mstr[1]),"UnitE": mstr[3],"P": float(mstr[5]),"UnitP": mstr[7],"validity": mstr[9],"Time": current_time}
                payload = {"profinet_name":msg.topic,"E": float(mstr[1]),"UnitE": mstr[3],"P": float(mstr[5]),"UnitP": mstr[7],"validity": mstr[9],"Time": mstr[11]}
                print(payload)
                return payload
            except :
                return "F"
        else:
            print("length of string does not match")
            return "F"
    except json.JSONDecodeError:
        return "F"
    
#################################################################################
#################################################################################
# received string from PLC: "value;TRUE;V;FALSE"
def json_convert_dido(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE',"True").replace('FALSE',"False").split(";")
        print(len(mstr))
        print(mstr)
        print(len(mstr))
        if len(mstr) == 6:
            try:
                current_time = str(datetime.datetime.now())
                # payload = {"profinet_name":msg.topic,"value": mstr[1], "validity": mstr[3], "Time": current_time}
                payload = {"profinet_name":msg.topic,"value": mstr[1], "validity": mstr[3], "Time": mstr[5]}
                print(payload)
                return payload
            except :
                return "F"
        else:
            print("length of string does not match")
            return "F"
    except json.JSONDecodeError:
        print("ridi")
        return "F"



######################################################

def mqtt_client_thread(topic):
    def on_connect(client, userdata, flags, rc):
        print(f"Threading for topic:{topic}. Connected to MQTT Broker with result code {rc}////////")
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        message=msg
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if topic in [Topic_EM1,Topic_EM2]:
            payload=json_convert_energy(message)
            threading.Thread(target=send_to_django_server_energy, args=(payload,)).start()
        elif topic in [Topic_LDH_edgeA1,Topic_LDH_edgeA2,Topic_LDH_edgeA3,Topic_LDH_edgeB1,Topic_LDH_edgeB2,Topic_LDH_edgeB3,Topic_LDH_network,Topic_LDH_energy]:
            payload = json_convert_temp(message)
            threading.Thread(target=send_to_django_server_temp, args=(payload,)).start()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, 1883, 60)
    client.loop_forever()  # Starts network loop


#################################### Temperature sensor topics #############################################
Topic_LDH_edgeA1=pre_profinet_name+ "---BT01"
Topic_LDH_edgeA2=pre_profinet_name+ "---BT02"
Topic_LDH_edgeA3=pre_profinet_name+ "---BT03"
Topic_LDH_edgeB1=pre_profinet_name+ "---BT04"
Topic_LDH_edgeB2=pre_profinet_name+ "---BT05"
Topic_LDH_edgeB3=pre_profinet_name+ "---BT06"
Topic_LDH_network=pre_profinet_name+"---BT07"
Topic_LDH_energy=pre_profinet_name+ "---BT08"
################################### Energy sensor Topics #################################

Topic_EM1=pre_profinet_name+"---PG01"
Topic_EM2=pre_profinet_name+"---PG02"

################################### Door sensor Topics #################################

Topic_door_sensor_edge_AF=pre_profinet_name+"---BGE1"
Topic_door_sensor_edge_AB=pre_profinet_name+"---BGE2"
Topic_door_sensor_edge_BF=pre_profinet_name+"---BGE3"
Topic_door_sensor_edge_BB=pre_profinet_name+"---BGE4"
Topic_door_sensor_network=pre_profinet_name+"---BGE5"
Topic_door_sensor_energy=pre_profinet_name+"---BGE6"
Topic_door_sensor_ACF=pre_profinet_name+"---BGE7"
Topic_door_sensor_ACB=pre_profinet_name+"---BGE8"
################################### Door Button Topics #################################
Topic_door_button_edge_AF=pre_profinet_name+"---SF01"
Topic_door_button_edge_AB=pre_profinet_name+"---SF02"
Topic_door_button_edge_BF=pre_profinet_name+"---SF03"
Topic_door_button_edge_BB=pre_profinet_name+"---SF04"
Topic_door_button_network=pre_profinet_name+"---SF05"
Topic_door_button_energy=pre_profinet_name+"---SF06"
Topic_door_button_ACF=pre_profinet_name+"---SF07"
Topic_door_button_ACB=pre_profinet_name+"---SF08"
################################### Latch sensor topics #################################
Topic_latch_sensor_edge_AF=pre_profinet_name+"---BGT1"	
Topic_latch_sensor_edge_AB=pre_profinet_name+"---BGT2"	
Topic_latch_sensor_edge_BF=pre_profinet_name+"---BGT3"	
Topic_latch_sensor_edge_BB=pre_profinet_name+"---BGT4"	
Topic_latch_sensor_network=pre_profinet_name+"---BGT5"	
Topic_latch_sensor_energy=pre_profinet_name+"---BGT6"	
Topic_latch_sensor_ACF=pre_profinet_name+"---BGT7"
Topic_latch_sensor_ACB=pre_profinet_name+"---BGT8"	
###################################### Latch topics###################
Topic_latch_edge_AF=pre_profinet_name+"---MB01"
Topic_latch_edge_AB=pre_profinet_name+"---MB02"
Topic_latch_edge_BF=pre_profinet_name+"---MB03"
Topic_latch_edge_BB=pre_profinet_name+"---MB04"
Topic_latch_network=pre_profinet_name+"---MB05"
Topic_latch_energy=pre_profinet_name+"---MB06"
Topic_latch_ACF=pre_profinet_name+"---MB07"
Topic_latch_ACB=pre_profinet_name+"---MB08"
####################################### LED topics ##################
Topic_LED_edge_AF=pre_profinet_name+"---PF01"
Topic_LED_edge_AB=pre_profinet_name+"---PF02"
Topic_LED_edge_BF=pre_profinet_name+"---PF03"
Topic_LED_edge_BB=pre_profinet_name+"---PF04"
Topic_LED_network=pre_profinet_name+"---PF05"
Topic_LED_energy=pre_profinet_name+"---PF06"
Topic_LED_ACF=pre_profinet_name+"---PF07"
Topic_LED_ACB=pre_profinet_name+"---PF08"

################################ Cooling alarm sensors #################
Topic_ACM1=pre_profinet_name+"---BG01"
Topic_ACM2=pre_profinet_name+"---BG02"



topics = [Topic_door_sensor_edge_AF, Topic_door_sensor_edge_AB, Topic_door_sensor_edge_BF, Topic_door_sensor_edge_BB, Topic_door_sensor_network, \
    Topic_door_sensor_energy, Topic_door_sensor_ACF, Topic_door_sensor_ACB, Topic_latch_sensor_edge_AF, Topic_latch_sensor_edge_AB, Topic_latch_sensor_edge_BF,\
        Topic_latch_sensor_edge_BB, Topic_latch_sensor_network, Topic_latch_sensor_energy, Topic_latch_sensor_ACF, Topic_latch_sensor_ACB, Topic_LED_edge_AF,\
            Topic_LED_edge_AB,Topic_LED_edge_BF, Topic_LED_edge_BB, Topic_LED_network, Topic_LED_energy, Topic_LED_ACF,Topic_LED_ACB, Topic_ACM1,Topic_ACM2,\
                Topic_door_button_edge_AF, Topic_door_button_edge_AB, Topic_door_button_edge_BF, Topic_door_button_edge_BB,Topic_door_button_ACF,\
                    Topic_door_button_ACB, Topic_door_button_network, Topic_door_button_energy]

topics_latch = [Topic_latch_edge_AF,Topic_latch_edge_AB,Topic_latch_edge_BF,Topic_latch_edge_BB,Topic_latch_network,Topic_latch_energy,Topic_latch_ACF,Topic_latch_ACB]
#################################################################################

topics_interval = [Topic_LDH_edgeA1, Topic_LDH_edgeA2, Topic_LDH_edgeA3, Topic_LDH_edgeB1, Topic_LDH_edgeB2, Topic_LDH_edgeB3, Topic_LDH_network, Topic_LDH_energy,Topic_EM1,Topic_EM2]
threads = []

for topic in topics_interval:
    t = threading.Thread(target=mqtt_client_thread, args=(topic,))
    t.start()
    threads.append(t)


def on_connect(client, userdata, flags, rc):
    print(f"Main Thread: Connected with result code {rc}")

    for topic in topics:
        client.subscribe(topic)
    for topic in topics_latch:
        client.subscribe(topic)



def on_message(client, userdata, msg):
    print(f"Main Message:msg",msg)
    if msg.topic in topics:
        print("topic is",msg.topic)
        print("message received")
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass


    elif msg.topic in topics_latch:
        print("topic is",msg.topic)
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass
    else:
        print("Fault")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()

