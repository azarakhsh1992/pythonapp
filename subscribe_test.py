
import paho.mqtt.client as mqtt
import time
import datetime

previous_time1 = None  # Initialize previous_time variable
previous_time2 = None  # Initialize previous_time variable
cyclic_msg_temp = []

PLC_name = "PLC1"


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
    global previous_time1 
    global previous_time2
    global cyclic_msg_temp

    
    cyclic_msg_energy = []
    
    if msg.topic == Topic1:
        print(f"Received message from {Topic1}: {msg.payload.decode()}")        
    elif msg.topic == Topic2:
        print(f"Received message from {Topic2}: {msg.payload.decode()}")        
    elif msg.topic == Topic3:
            print(f"Received message from {Topic3}: {msg.payload.decode()}")
    elif msg.topic == Topic4:
            print(f"Received message from {Topic4}: {msg.payload.decode()}")
    elif msg.topic == Topic5:
            print(f"Received message from {Topic5}: {msg.payload.decode()}")
    elif msg.topic == Topic6:
            print(f"Received message from {Topic6}: {msg.payload.decode()}")
    elif msg.topic == Topic7:
            print(f"Received message from {Topic7}: {msg.payload.decode()}")
    elif msg.topic == Topic8:
            print(f"Received message from {Topic8}: {msg.payload.decode()}")
    elif msg.topic == Topic9:
            print(f"Received message from {Topic9}: {msg.payload.decode()}")
    elif msg.topic == Topic10:
            print(f"Received message from {Topic10}: {msg.payload.decode()}")
    elif msg.topic == Topic11:
            print(f"Received message from {Topic11}: {msg.payload.decode()}")
    elif msg.topic == Topic12:
            print(f"Received message from {Topic12}: {msg.payload.decode()}")
    elif msg.topic == Topic13:
            print(f"Received message from {Topic13}: {msg.payload.decode()}")
    elif msg.topic == Topic14:
            print(f"Received message from {Topic14}: {msg.payload.decode()}")
    elif msg.topic == Topic15:
            print(f"Received message from {Topic15}: {msg.payload.decode()}")
    elif msg.topic == Topic16:
            print(f"Received message from {Topic16}: {msg.payload.decode()}")
    elif msg.topic == Topic17:
            print(f"Received message from {Topic17}: {msg.payload.decode()}")
    elif msg.topic == Topic18:
            print(f"Received message from {Topic18}: {msg.payload.decode()}")
    elif msg.topic == Topic19:
            print(f"Received message from {Topic19}: {msg.payload.decode()}")
    elif msg.topic == Topic20:
            print(f"Received message from {Topic20}: {msg.payload.decode()}")
    elif msg.topic == Topic21:
            print(f"Received message from {Topic21}: {msg.payload.decode()}")
    elif msg.topic == Topic22:
            print(f"Received message from {Topic22}: {msg.payload.decode()}")
    elif msg.topic == Topic23:
            print(f"Received message from {Topic23}: {msg.payload.decode()}")
    elif msg.topic == Topic24:
            print(f"Received message from {Topic24}: {msg.payload.decode()}")
    elif msg.topic == Topic25:
            print(f"Received message from {Topic25}: {msg.payload.decode()}")
    elif msg.topic == Topic26:
            print(f"Received message from {Topic26}: {msg.payload.decode()}")
    elif msg.topic == Topic27:
            print(f"Received message from {Topic27}: {msg.payload.decode()}")
    elif msg.topic == Topic28:
            print(f"Received message from {Topic28}: {msg.payload.decode()}")
    elif msg.topic == Topic29:
            print(f"Received message from {Topic29}: {msg.payload.decode()}")
    elif msg.topic == Topic30:
            print(f"Received message from {Topic30}: {msg.payload.decode()}")
    elif msg.topic == Topic31:
            print(f"Received message from {Topic31}: {msg.payload.decode()}")
    elif msg.topic == Topic32:
            print(f"Received message from {Topic32}: {msg.payload.decode()}")
    elif msg.topic == Topic33:
            print(f"Received message from {Topic33}: {msg.payload.decode()}")
    elif msg.topic == Topic34:
            print(f"Received message from {Topic34}: {msg.payload.decode()}")
    elif msg.topic == Topic35:
            print(f"Received message from {Topic35}: {msg.payload.decode()}")
    elif msg.topic == Topic36:
            print(f"Received message from {Topic36}: {msg.payload.decode()}")
    elif msg.topic == Topic37:
            print(f"Received message from {Topic37}: {msg.payload.decode()}")
    elif msg.topic == Topic38:
            print(f"Received message from {Topic38}: {msg.payload.decode()}")
    elif msg.topic == Topic39:
            print(f"Received message from {Topic39}: {msg.payload.decode()}")
    elif msg.topic == Topic40:
            print(f"Received message from {Topic40}: {msg.payload.decode()}")
    elif msg.topic == Topic41:
            print(f"Received message from {Topic41}: {msg.payload.decode()}")
    elif msg.topic == Topic42:
            print(f"Received message from {Topic42}: {msg.payload.decode()}")
    elif msg.topic == Topic43:
            print(f"Received message from {Topic43}: {msg.payload.decode()}")
    elif msg.topic == Topic44:
            print(f"Received message from {Topic44}: {msg.payload.decode()}")
    elif msg.topic == Topic45:
            print(f"Received message from {Topic45}: {msg.payload.decode()}")
    elif msg.topic == Topic46:
            print(f"Received message from {Topic46}: {msg.payload.decode()}")
    elif msg.topic == Topic47:
            print(f"Received message from {Topic47}: {msg.payload.decode()}")
    elif msg.topic == Topic48:
            print(f"Received message from {Topic48}: {msg.payload.decode()}")
    elif msg.topic == Topic49:
            print(f"Received message from {Topic49}: {msg.payload.decode()}")
    elif msg.topic == Topic50:
            print(f"Received message from {Topic50}: {msg.payload.decode()}")
    elif msg.topic == Topic51:
            print(f"Received message from {Topic51}: {msg.payload.decode()}")
    elif msg.topic == Topic52:
            print(f"Received message from {Topic52}: {msg.payload.decode()}")
    elif msg.topic == Topic53:
            print(f"Received message from {Topic53}: {msg.payload.decode()}")
    elif msg.topic == Topic54:
            print(f"Received message from {Topic54}: {msg.payload.decode()}")
    elif msg.topic == Topic55:
            print(f"Received message from {Topic55}: {msg.payload.decode()}")
    elif msg.topic == Topic56:
            print(f"Received message from {Topic56}: {msg.payload.decode()}")
    elif msg.topic == Topic57:
            print(f"Received message from {Topic57}: {msg.payload.decode()}")
    elif msg.topic == Topic58:
            print(f"Received message from {Topic58}: {msg.payload.decode()}")
    
    elif msg.topic == Topic_LDH_edgeA1:
        topic_temp1 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeA1))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp1)
        
    elif msg.topic == Topic_LDH_edgeA2:
        topic_temp2 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeA2))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp2)
        
    elif msg.topic == Topic_LDH_edgeA3:
        topic_temp3 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeA3))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp3)
    elif msg.topic == Topic_LDH_edgeB1:
        topic_temp4 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeB1))
        except  ValueError:
            pass
        cyclic_msg_temp.append(topic_temp4)
    elif msg.topic == Topic_LDH_edgeB2:
        topic_temp5 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeB2))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp5)
    elif msg.topic == Topic_LDH_edgeB3:
        topic_temp6 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_edgeB3))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp6)
    elif msg.topic == Topic_LDH_network:
        topic_temp7 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_network))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp7)
    elif msg.topic == Topic_LDH_energy:
        topic_temp8 = msg.payload.decode()
        try:
            cyclic_msg_temp.pop(cyclic_msg_temp.index(Topic_LDH_energy))
        except ValueError:
            pass
        cyclic_msg_temp.append(topic_temp8)
        
    print(cyclic_msg_temp)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.1", 1883, 60)
client.loop_forever()
