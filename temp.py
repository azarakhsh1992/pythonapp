
import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests
import os
import certifi

# PLC_name = "KAAASDASASDVDASDASACAD"
PLC_name = "KAAASDASASDVDASDASACAD"
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


#################################################################################
Topic_LDH_edgeA1=pre_profinet_name+'SSDSDVA'
Topic_LDH_edgeA2=pre_profinet_name+"LDH_edgeA2"
Topic_LDH_edgeA3=pre_profinet_name+"AFREWFF"
Topic_LDH_edgeB1=pre_profinet_name+"LDH_edgeB1"
Topic_LDH_edgeB2=pre_profinet_name+"LDH_edgeB2"
Topic_LDH_edgeB3=pre_profinet_name+"LDH_edgeB3"
Topic_LDH_network=pre_profinet_name+"LDH_network"
Topic_LDH_energy="LDH_network"

Topic_EM1=pre_profinet_name+"SVDFSVF"
Topic_EM2=pre_profinet_name+"GXBXGFN"


Topic_door_sensor_edge_AF=pre_profinet_name+"1111111"
Topic_door_sensor_edge_AB=pre_profinet_name+"SFAFAAS"
Topic_door_sensor_edge_BF=pre_profinet_name+"VDASVSV"
Topic_door_sensor_edge_BB=pre_profinet_name+"SVVSDVS"
Topic_door_sensor_network=pre_profinet_name+"SHTETAG"
Topic_door_sensor_energy=pre_profinet_name+"STHSTHR"
Topic_door_sensor_ACF=pre_profinet_name+"DFDDFDF"
Topic_door_sensor_ACB=pre_profinet_name+"door_sensor_ACB"

Topic_latch_sensor_edge_AF=pre_profinet_name+"latch_sensor_edgeAF"	
Topic_latch_sensor_edge_AB=pre_profinet_name+"latch_sensor_edgeAB"	
Topic_latch_sensor_edge_BF=pre_profinet_name+"latch_sensor_edgeBF"	
Topic_latch_sensor_edge_BB=pre_profinet_name+"latch_sensor_edgeBB"	
Topic_latch_sensor_network=pre_profinet_name+"latch_sensor_network"	
Topic_latch_sensor_energy=pre_profinet_name+"latch_sensor_energy"	
Topic_latch_sensor_ACF=pre_profinet_name+"latch_sensor_ACF"	
Topic_latch_sensor_ACB=pre_profinet_name+"latch_sensor_ACB"	
######################################Latch topics###################
Topic_latch_edge_AF=pre_profinet_name+"latch_edge_AF"
Topic_latch_edge_AB=pre_profinet_name+"latch_edge_AB"
Topic_latch_edge_BF=pre_profinet_name+"latch_edge_BF"
Topic_latch_edge_BB=pre_profinet_name+"latch_edge_BB"
Topic_latch_network=pre_profinet_name+"latch_network"
Topic_latch_energy=pre_profinet_name+"latch_energy"
Topic_latch_ACF=pre_profinet_name+"ASDASDD"
Topic_latch_ACB=pre_profinet_name+"FNGSGHG"
#########################################################
Topic_LED_edge_AF=pre_profinet_name+"DSADASA"
Topic_LED_edge_AB=pre_profinet_name+"LED_1_edgeAB"
Topic_LED_edge_BF=pre_profinet_name+"LED_1_edgeBF"
Topic_LED_edge_BB=pre_profinet_name+"LED_1_edgeBB"
Topic_LED_network=pre_profinet_name+"LED_1_network"
Topic_LED_energy=pre_profinet_name+"LED_1_energy"
Topic_LED_ACF=pre_profinet_name+"LED_1_ACF"
Topic_LED_ACB=pre_profinet_name+"LED_1_ACB"


Topic57=pre_profinet_name+"AC_sensor1"
Topic58=pre_profinet_name+"AC_sensor2"

topics = [Topic_door_sensor_edge_AF, Topic_door_sensor_edge_AB, Topic_door_sensor_edge_BF, Topic_door_sensor_edge_BB, Topic_door_sensor_network, \
    Topic_door_sensor_energy, Topic_door_sensor_ACF, Topic_door_sensor_ACB, Topic_latch_sensor_edge_AF, Topic_latch_sensor_edge_AB, Topic_latch_sensor_edge_BF,\
        Topic_latch_sensor_edge_BB, Topic_latch_sensor_network, Topic_latch_sensor_energy, Topic_latch_sensor_ACF, Topic_latch_sensor_ACB, Topic_LED_edge_AF,\
            Topic_LED_edge_AB,Topic_LED_edge_BF, Topic_LED_edge_BB, Topic_LED_network, Topic_LED_energy, Topic_LED_ACF,Topic_LED_ACB,\
                Topic57,Topic58,Topic_latch_edge_AF,Topic_latch_edge_AB,Topic_latch_edge_BF,Topic_latch_edge_BB,Topic_latch_network,Topic_latch_energy,Topic_latch_ACF,Topic_latch_ACB]

#################################################################################

topics_interval = [Topic_LDH_edgeA1, Topic_LDH_edgeA2, Topic_LDH_edgeA3, Topic_LDH_edgeB1, Topic_LDH_edgeB2, Topic_LDH_edgeB3, Topic_LDH_network, Topic_LDH_energy]
threads = []

messages_interval = []
timer_running = False

def process_messages_interval():
    global messages_interval, timer_running
    # Process all messages together
    payloads = [json_convert_dido(msg) for msg in messages_interval]
    combined_payload = json.dumps(payloads)  # Combine into one JSON object
    print("##########################################")
    print(combined_payload)
    print(type(combined_payload))
    python_data = json.loads(combined_payload)
    print(python_data)
    print(type(python_data))
    send_to_django_server_dido(combined_payload)  # Send to Django server
    messages_interval = []  # Reset the list
    timer_running = False


def on_connect(client, userdata, flags, rc):
    print(f"Main Thread: Connected with result code {rc}")

    for topic in topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    global timer_running ,messages_interval
    print(f"Main Message:msg",msg)
    if msg.topic in topics_interval:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass
    elif msg.topic in [Topic_EM1,Topic_EM2]:
            payload=json_convert_energy(msg)
            if payload !="F":
                threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
            else:
                pass
            
    elif msg.topic in topics:
        messages_interval.append(msg)
        if not timer_running:
            timer_running = True
            # Start a timer for 30 seconds
            threading.Timer(5, process_messages_interval).start()
    else:
        print("Fault")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()
