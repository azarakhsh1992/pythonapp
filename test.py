import _sqlite3
import requests
import json

def read_value():
    serial_1 = "/iolinkmaster/port[1]/iolinkdevice/serial"
    serial_2 = "/iolinkmaster/port[2]/iolinkdevice/serial"
    serial_3 = "/iolinkmaster/port[3]/iolinkdevice/serial"
    serial_4 = "/iolinkmaster/port[4]/iolinkdevice/serial"
    serial_5 = "/iolinkmaster/port[5]/deviceinfo/serialnumber"
    serial_6 = "/iolinkmaster/port[6]/iolinkdevice/serial"
    serial_7 = "/iolinkmaster/port[7]/iolinkdevice/serial"
    serial_8 = "/iolinkmaster/port[8]/iolinkdevice/serial"
    port_1 = "/iolinkmaster/port[1]/iolinkdevice/pdin/"
    port_2 = "/iolinkmaster/port[2]/iolinkdevice/pdin/"
    port_3 = "/iolinkmaster/port[3]/iolinkdevice/pdin/"
    port_4 = "/iolinkmaster/port[4]/iolinkdevice/pdin/"
    port_5 = "/iolinkmaster/port[5]/iolinkdevice/pdin//"
    port_6 = "/iolinkmaster/port[6]/iolinkdevice/pdin/"
    port_7 = "/iolinkmaster/port[7]/iolinkdevice/pdin/"
    port_8 = "/iolinkmaster/port[8]/iolinkdevice/pdout/"
    payload_read = {"code":"request","cid":4711,"adr":"/getdatamulti",\
               "data":{\
                   "datatosend":[ serial_1, port_1, serial_2, port_2,serial_3,port_3,serial_4,port_4,serial_5,port_5,\
                       serial_6,port_6, serial_7,port_7,serial_8,port_8]
                   }
               }
    payload_write = { "code":"request", "cid":10, "adr":"iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"} }
    headers = {}
    headers['Content-Type'] = 'application/json'

    try:
        response = requests.post(url='http://192.168.0.4', data=json.dumps(payload_read), headers=None)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        responses =response.json()
        # print(responses)
        # print(response)
        # pretty_json = json.dumps(responses, indent=4)
        # print(pretty_json)
        # print(type(pretty_json))

        # response2 = requests.post(url='http://192.168.0.4', data=json.dumps(payload_write), headers=None)
        # response2.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        # responses2 =response2.json()
        # print(responses2)
        # print(response2)
        # pretty_json2 = json.dumps(responses2, indent=4)
        # print(pretty_json2)
        # print(type(pretty_json2))
        # return response2.json(),response.json()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise e

def write_value():
        payload_write = { "code":"request", "cid":10, "adr":"iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"} }
        response2 = requests.post(url='http://192.168.0.4', data=json.dumps(payload_write), headers=None)
        response2.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        responses2 =response2.json()
        print(responses2)
        print(response2)
        # pretty_json2 = json.dumps(responses2, indent=4)
        # print(pretty_json2)
        # print(type(pretty_json2))
        return response2.json()

read_value()
# write_value()