
import paho.mqtt.client as mqtt
import time
import datetime

previous_time1 = None  # Initialize previous_time variable
previous_time2 = None  # Initialize previous_time variable


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

Topic_AC_sensor1=PLC_name+"AC_sensor1"
Topic_AC_sensor2=PLC_name+"AC_sensor2"


Topic_door_sensor_edgeAF=PLC_name+"door_sensor_edgeAF"
Topic_door_sensor_edgeAB=PLC_name+"door_sensor_edgeAB"
Topic_door_sensor_edgeBF=PLC_name+"door_sensor_edgeBF"
Topic_door_sensor_edgeBB=PLC_name+"door_sensor_edgeBB"
Topic_door_sensor_network=PLC_name+"door_sensor_network"
Topic_door_sensor_energy=PLC_name+"door_sensor_energy"
Topic_door_sensor_ACF=PLC_name+"door_sensor_ACF"
Topic_door_sensor_ACB=PLC_name+"door_sensor_ACB"


Topic_latch_sensor_edgeAF=PLC_name+"latch_sensor_edgeAF"	
Topic_latch_sensor_edgeAB=PLC_name+"latch_sensor_edgeAB"	
Topic_latch_sensor_edgeBF=PLC_name+"latch_sensor_edgeBF"	
Topic_latch_sensor_edgeBB=PLC_name+"latch_sensor_edgeBB"	
Topic_latch_sensor_network=PLC_name+"latch_sensor_network"	
Topic_latch_sensor_energy=PLC_name+"latch_sensor_energy"	
Topic_latch_sensor_ACF=PLC_name+"latch_sensor_ACF"	
Topic_latch_sensor_ACB=PLC_name+"latch_sensor_ACB"	

Topic_latch_edgeAF=PLC_name+"latch_edge_AF"
Topic_latch_edgeAB=PLC_name+"latch_edge_AB"
Topic_latch_edgeBF=PLC_name+"latch_edge_BF"
Topic_latch_edgeBB=PLC_name+"latch_edge_BB"
Topic_latch_network=PLC_name+"latch_network"
Topic_latch_energy=PLC_name+"latch_energy"
Topic_latch_ACF=PLC_name+"latch_ACF"
Topic_latch_ACB=PLC_name+"latch_ACB"

Topic_LED_1_edgeAF=PLC_name+"LED_1_edgeAF"
Topic_LED_2_edgeAF=PLC_name+"LED_2_edgeAF"
Topic_LED_3_edgeAF=PLC_name+"LED_3_edgeAF"
Topic_LED_4_edgeAF=PLC_name+"LED_4_edgeAF"

Topic_LED_1_edgeAB=PLC_name+"LED_1_edgeAB"
Topic_LED_2_edgeAB=PLC_name+"LED_2_edgeAB"
Topic_LED_3_edgeAB=PLC_name+"LED_3_edgeAB"
Topic_LED_4_edgeAB=PLC_name+"LED_4_edgeAB"

Topic_LED_1_edgeBF=PLC_name+"LED_1_edgeBF"
Topic_LED_2_edgeBF=PLC_name+"LED_2_edgeBF"
Topic_LED_3_edgeBF=PLC_name+"LED_3_edgeBF"
Topic_LED_4_edgeBF=PLC_name+"LED_4_edgeBF"

Topic_LED_1_edgeBB=PLC_name+"LED_1_edgeBB"
Topic_LED_2_edgeBB=PLC_name+"LED_2_edgeBB"
Topic_LED_3_edgeBB=PLC_name+"LED_3_edgeBB"
Topic_LED_4_edgeBB=PLC_name+"LED_4_edgeBB"

Topic_LED_1_network=PLC_name+"LED_1_network"
Topic_LED_2_network=PLC_name+"LED_2_network"
Topic_LED_3_network=PLC_name+"LED_3_network"
Topic_LED_4_network=PLC_name+"LED_4_network"

Topic_LED_1_energy=PLC_name+"LED_1_energy"
Topic_LED_2_energy=PLC_name+"LED_2_energy"
Topic_LED_3_energy=PLC_name+"LED_3_energy"
Topic_LED_4_energy=PLC_name+"LED_4_energy"

Topic_LED_1_ACF=PLC_name+"LED_1_ACF"
Topic_LED_2_ACF=PLC_name+"LED_2_ACF"
Topic_LED_3_ACF=PLC_name+"LED_3_ACF"
Topic_LED_4_ACF=PLC_name+"LED_4_ACF"

Topic_LED_1_ACB=PLC_name+"LED_1_ACB"
Topic_LED_2_ACB=PLC_name+"LED_2_ACB"
Topic_LED_3_ACB=PLC_name+"LED_3_ACB"
Topic_LED_4_ACB=PLC_name+"LED_4_ACB"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to multiple topics

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
    
    
    client.subscribe(Topic_AC_sensor1)
    client.subscribe(Topic_AC_sensor2)
    
    
    client.subscribe(Topic_door_sensor_edgeAF)
    client.subscribe(Topic_door_sensor_edgeAB)
    client.subscribe(Topic_door_sensor_edgeBF)
    client.subscribe(Topic_door_sensor_edgeBB)
    client.subscribe(Topic_door_sensor_network)
    client.subscribe(Topic_door_sensor_energy)
    client.subscribe(Topic_door_sensor_ACF)
    client.subscribe(Topic_door_sensor_ACB)
    
    client.subscribe(Topic_door_sensor_ACB)
    
    
    
    




def on_message(client, userdata, msg):
    global previous_time1 
    global previous_time2
    if msg.topic == topic1:
        current_time1 = datetime.datetime.now().second
        print(f"current time Topic1: {current_time1}")

        if previous_time1 is not None:
            time_difference1 = current_time1 - previous_time1
            print(f"Time difference Topic1 : {time_difference1}")

        # else:
            pass
        previous_time1 = current_time1
        print(f"Received message from {topic1}: {msg.payload.decode()}")        
    elif msg.topic == topic2:
        current_time2 = datetime.datetime.now().second
        print(f"current time Topic2: {current_time2}")
        if previous_time2 is not None:
            time_difference2 = (current_time2 - previous_time2)
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
