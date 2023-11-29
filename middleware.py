
import paho.mqtt.client as mqtt
import time
import datetime
import threading
import json
import requests
import os   

PLC_name = "KAAASDASASDVDASDASACAD"
pre_profinet_name = PLC_name[:-7]
broker = 'localhost'
django_url = 'http://localhost:8000/web/mqttmiddleware/'
#######################################################
#to close the door after it got open
def delayed_publish(client, module_topic):
        time.sleep(3)
        this_topic = pre_profinet_name
        this_message = module_topic+';False'
        client.publish(this_topic, this_message)

##############################################################
def send_to_django_server_dido(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'dido/'
    headers = {'Content-type': 'application/json'}
    print("here")
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers,)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}", e.response.text)
            
    else:
        pass
    ##############################################################
def send_to_django_server_temp(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'temp/'
    headers = {'Content-Type': 'application/json'}
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}", e.response.text)
    else:
        pass
    ##############################################################
def send_to_django_server_energy(payload):
    # Define the URL of your Django server endpoint
    this_url = django_url+'energy/'
    headers = {'Content-Type': 'application/json'}
    if payload != "F":
        try:
            response = requests.post(url=this_url, json=payload, headers=headers)
            response.raise_for_status()
            # Handle successful request
            print(response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle exceptions for the HTTP request here
            print(f"Failed to send data to Django server: {e}", e.response.text)
    else:
        pass
#################################################################################
# received string from PLC: "T;25;Tmin;15.5;Tmax;32.4;RH;56.5;V;FALSE;Time;65468451sacc"
def json_convert_temp(msg):
    try:
        mstr=msg.payload.decode().replace('TRUE',"True").replace('FALSE',"False").split(";")
        print(len(mstr))
        if len(mstr) == 10:
            try:
                current_time = str(datetime.datetime.now())
                payload = {"profinet_name":msg.topic,"T": float(mstr[1]),"Tmin": float(mstr[3]),"Tmax": float(mstr[5]),"RH": float(mstr[7]),"V": mstr[9],"Time": current_time}
                # payload = {"profinet_name":msg.topic,"T": float(mstr[1]),"Tmin": float(mstr[3]),"Tmax": float(mstr[5]),"RH": float(mstr[7]),"V": mstr[9],"Time": mstr[11]}
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
        if len(mstr) == 10:
            try:
                current_time = str(datetime.datetime.now())
                payload = {"profinet_name":msg.topic,"E": float(mstr[1]),"UnitE": mstr[3],"P": float(mstr[5]),"UnitP": mstr[7],"V": mstr[9],"Time": current_time}
                # payload = {"profinet_name":msg.topic,"E": float(mstr[1]),"UnitE": mstr[3],"P": float(mstr[5]),"UnitP": mstr[7],"V": mstr[9],"Time": mstr[11]}
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
        if len(mstr) == 4:
            try:
                current_time = str(datetime.datetime.now())
                payload = {"profinet_name":msg.topic,"value": mstr[1], "V": mstr[3], "Time": current_time}
                # payload = {"profinet_name":msg.topic,"value": mstr[1], "V": mstr[3], "Time": mstr[5]}
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


Topic1=pre_profinet_name+"1111111"
Topic2=pre_profinet_name+"SFAFAAS"
Topic3=pre_profinet_name+"VDASVSV"
Topic4=pre_profinet_name+"SVVSDVS"
Topic5=pre_profinet_name+"SHTETAG"
Topic6=pre_profinet_name+"STHSTHR"
Topic7=pre_profinet_name+"DFDDFDF"
Topic8=pre_profinet_name+"door_sensor_ACB"

Topic9=pre_profinet_name+"latch_sensor_edgeAF"	
Topic10=pre_profinet_name+"latch_sensor_edgeAB"	
Topic11=pre_profinet_name+"latch_sensor_edgeBF"	
Topic12=pre_profinet_name+"latch_sensor_edgeBB"	
Topic13=pre_profinet_name+"latch_sensor_network"	
Topic14=pre_profinet_name+"latch_sensor_energy"	
Topic15=pre_profinet_name+"latch_sensor_ACF"	
Topic16=pre_profinet_name+"latch_sensor_ACB"	
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
Topic25=pre_profinet_name+"LED_1_edgeAF"
Topic26=pre_profinet_name+"LED_2_edgeAF"
Topic27=pre_profinet_name+"LED_3_edgeAF"
Topic28=pre_profinet_name+"LED_4_edgeAF"

Topic29=pre_profinet_name+"LED_1_edgeAB"
Topic30=pre_profinet_name+"LED_2_edgeAB"
Topic31=pre_profinet_name+"LED_3_edgeAB"
Topic32=pre_profinet_name+"LED_4_edgeAB"

Topic33=pre_profinet_name+"LED_1_edgeBF"
Topic34=pre_profinet_name+"LED_2_edgeBF"
Topic35=pre_profinet_name+"LED_3_edgeBF"
Topic36=pre_profinet_name+"LED_4_edgeBF"

Topic37=pre_profinet_name+"LED_1_edgeBB"
Topic38=pre_profinet_name+"LED_2_edgeBB"
Topic39=pre_profinet_name+"LED_3_edgeBB"
Topic40=pre_profinet_name+"LED_4_edgeBB"

Topic41=pre_profinet_name+"LED_1_network"
Topic42=pre_profinet_name+"LED_2_network"
Topic43=pre_profinet_name+"LED_3_network"
Topic44=pre_profinet_name+"LED_4_network"

Topic45=pre_profinet_name+"LED_1_energy"
Topic46=pre_profinet_name+"LED_2_energy"
Topic47=pre_profinet_name+"LED_3_energy"
Topic48=pre_profinet_name+"LED_4_energy"

Topic49=pre_profinet_name+"LED_1_ACF"
Topic50=pre_profinet_name+"LED_2_ACF"
Topic51=pre_profinet_name+"LED_3_ACF"
Topic52=pre_profinet_name+"LED_4_ACF"

Topic53=pre_profinet_name+"LED_1_ACB"
Topic54=pre_profinet_name+"LED_2_ACB"
Topic55=pre_profinet_name+"LED_3_ACB"
Topic56=pre_profinet_name+"LED_4_ACB"

Topic57=pre_profinet_name+"AC_sensor1"
Topic58=pre_profinet_name+"AC_sensor2"

topics = [Topic1, Topic2, Topic3, Topic4, Topic5, Topic6, Topic7, Topic8, Topic9, Topic10, Topic11, Topic12, Topic13\
    , Topic14, Topic15, Topic16, Topic25, Topic26, Topic27, Topic28, Topic29, Topic30, Topic31, Topic32, Topic33, \
        Topic34, Topic35, Topic36, Topic37, Topic38, Topic39, Topic40, Topic41, Topic42, Topic43, Topic44, Topic45, \
            Topic46, Topic47, Topic48, Topic49, Topic50, Topic51, Topic52,Topic53,Topic54,Topic55,Topic56,Topic57,Topic58]

topics_latch = [Topic_latch_edge_AF,Topic_latch_edge_AB,Topic_latch_edge_BF,Topic_latch_edge_BB,Topic_latch_network,Topic_latch_energy,Topic_latch_ACF,]
#################################################################################

topics_interval = [Topic_LDH_edgeA1, Topic_LDH_edgeA2, Topic_LDH_edgeA3, Topic_LDH_edgeB1, Topic_LDH_edgeB2, Topic_LDH_edgeB3, Topic_LDH_network, Topic_LDH_energy,Topic_EM1,Topic_EM2,Topic_latch_ACB]
threads = []

for topic in topics_interval:
    t = threading.Thread(target=mqtt_client_thread, args=(topic,))
    t.start()
    threads.append(t)



def main_thread():
    def on_connect(client, userdata, flags, rc):
        print(f"Main_thread: Connected with result code {rc}")

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
                if payload.get('value') == "TRUE":  # Assuming the value is a boolean True
                    threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_AF)).start()
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


threading.Thread(target=main_thread).start()

# def on_connect(client, userdata, flags, rc):
#     print(f"Main Thread: Connected with result code {rc}")

#     for topic in topics:
#         client.subscribe(topic)
#     for topic in topics_latch:
#         client.subscribe(topic)



# def on_message(client, userdata, msg):
#     print(f"Main Message:msg",msg)
#     if msg.topic in topics:
#         print("topic is",msg.topic)
#         print("message received")
#         payload=json_convert_dido(msg)
#         if payload !="F":
#             threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
#         else:
#             print("fault")
#             pass


#     elif msg.topic in topics_latch:
#         print("topic is",msg.topic)
#         payload=json_convert_dido(msg)
#         if payload !="F":
#             threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
#             if payload.get('value') == "TRUE":  # Assuming the value is a boolean True
#                 threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_AF)).start()
#         else:
#             print("fault")
#             pass
#     else:
#         print("Fault")


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(broker, 1883, 60)
# client.loop_forever()

