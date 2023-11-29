
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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if topic in [Topic_EM1,Topic_EM2]:
            payload=json_convert_energy(message)
            threading.Thread(target=send_to_django_server_energy, args=(payload,)).start()
        elif topic in [Topic_LDH_edgeA1,Topic_LDH_edgeA2,Topic_LDH_edgeA3,Topic_LDH_edgeB1,Topic_LDH_edgeB2,Topic_LDH_edgeB3,Topic_LDH_network,Topic_LDH_energy]:
            payload = json_convert_temp(message)
            threading.Thread(target=send_to_django_server_temp, args=(payload,)).start()
        else:
            pass

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
Topic_latch_ACB=pre_profinet_name+"latch_ACB"
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
#################################################################################

topics = [Topic_LDH_edgeA1, Topic_LDH_edgeA2, Topic_LDH_edgeA3, Topic_LDH_edgeB1, Topic_LDH_edgeB2, Topic_LDH_edgeB3, Topic_LDH_network, Topic_LDH_energy,Topic_EM1,Topic_EM2]
threads = []

for topic in topics:
    t = threading.Thread(target=mqtt_client_thread, args=(topic,))
    t.start()
    threads.append(t)


def on_connect(client, userdata, flags, rc):
    print(f"Main Thread: Connected with result code {rc}")

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
    client.subscribe(Topic_latch_edge_AF)
    client.subscribe(Topic_latch_edge_AB)
    client.subscribe(Topic_latch_edge_BF)
    client.subscribe(Topic_latch_edge_BB)
    client.subscribe(Topic_latch_network)
    client.subscribe(Topic_latch_energy)
    client.subscribe(Topic_latch_ACF)
    client.subscribe(Topic_latch_ACB)
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
        print("message received")
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "True":  # Assuming the value is a boolean True
                delayed_publish(client,Topic1)
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic2:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic3:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic4:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic5:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic6:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic7:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic8:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic9:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic10:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic11:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic12:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic13:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic14:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic15:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic16:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_edge_AF:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_AF)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_edge_AB:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_AB)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_edge_BF:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_BF)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_edge_BB:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_edge_BB)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_network:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_network)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_energy:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_energy)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_ACF:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_ACF)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic_latch_ACB:
        payload=json_convert_dido(msg)
        if payload !="F":
            if payload.get('value') == "open":  # Assuming the value is a boolean True
                threading.Thread(target=delayed_publish, args=(client, Topic_latch_ACB)).start()
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic25:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic26:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
    
    
    
            pass
    elif msg.topic == Topic27:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic28:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic29:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic30:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic31:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic32:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic33:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic34:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic35:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic36:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic37:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic38:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic39:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic40:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic45:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic46:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic47:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic48:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic49:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic50:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic51:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic52:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic53:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic54:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic55:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic56:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic57:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass




    elif msg.topic == Topic58:
        payload=json_convert_dido(msg)
        if payload !="F":
            threading.Thread(target=send_to_django_server_dido, args=(payload,)).start()
        else:
            print("fault")
            pass



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()

