import _sqlite3
import requests
import json
import time


class Iolink():
    url = 'http://192.168.0.4'
    serial_1 = "/iolinkmaster/port[1]/iolinkdevice/serial"
    serial_2 = "/iolinkmaster/port[2]/iolinkdevice/serial"
    serial_3 = "/iolinkmaster/port[3]/iolinkdevice/serial"
    serial_4 = "/iolinkmaster/port[4]/iolinkdevice/serial"
    serial_5 = "/iolinkmaster/port[5]/deviceinfo/serialnumber"
    serial_6 = "/iolinkmaster/port[6]/iolinkdevice/serial"
    serial_7 = "/iolinkmaster/port[7]/iolinkdevice/serial"
    serial_8 = "/iolinkmaster/port[8]/iolinkdevice/serial"    
    
    deviceid_1 = "/iolinkmaster/port[1]/iolinkdevice/deviceid"
    deviceid_2 = "/iolinkmaster/port[2]/iolinkdevice/deviceid"
    deviceid_3 = "/iolinkmaster/port[3]/iolinkdevice/deviceid"
    deviceid_4 = "/iolinkmaster/port[5]/iolinkdevice/deviceid"
    deviceid_5 = "/iolinkmaster/port[5]/iolinkdevice/deviceid"
    deviceid_6 = "/iolinkmaster/port[6]/iolinkdevice/deviceid"
    deviceid_7 = "/iolinkmaster/port[7]/iolinkdevice/deviceid"
    deviceid_8 = "/iolinkmaster/port[8]/iolinkdevice/deviceid"
    
    value_1 = "/iolinkmaster/port[1]/iolinkdevice/pdin/"
    value_2 = "/iolinkmaster/port[2]/iolinkdevice/pdin/"
    value_3 = "/iolinkmaster/port[3]/iolinkdevice/pdin/"
    value_4 = "/iolinkmaster/port[4]/iolinkdevice/pdin/"
    value_5 = "/iolinkmaster/port[5]/iolinkdevice/pdin//"
    value_6 = "/iolinkmaster/port[6]/iolinkdevice/pdin/"
    value_7 = "/iolinkmaster/port[7]/iolinkdevice/pdin/"
    value_8 = "/iolinkmaster/port[8]/iolinkdevice/pdout/"
    payload_read = {"code": "request", "cid": 4711, "adr": "/getdatamulti",
                        "data": {
                            "datatosend": [serial_1,deviceid_1, value_1, serial_2,deviceid_2, value_2, serial_3,deviceid_3, value_3,deviceid_4,\
                                serial_4,deviceid_4, value_4,serial_5,deviceid_5, value_5, serial_6,deviceid_6, value_6, serial_7,deviceid_7,\
                                    value_7, serial_8,deviceid_8,value_8
                                    ]
                            }
                        }
    payload_write = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "01"}}
    payload_write2 = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "00"}}
    
    def read_value(self):
        headers = {}
        headers['Content-Type'] = 'application/json'

        try:
            response = requests.post(url='http://192.168.0.4', data=json.dumps(self.payload_read), headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            responses = response.json()
            # print(response)
            # print(responses)
            pretty_json = json.dumps(responses, indent=4)
            print(pretty_json)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def write_value(self):
        payload_write = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata",\
                        "data": {"newvalue": "01"}}
        response2 = requests.post(url='http://192.168.0.4', data=json.dumps(payload_write), headers=None)
        response2.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        responses2 = response2.json()
        print(response2)
        print(responses2)
        pretty_json2 = json.dumps(responses2, indent=4)
        print(pretty_json2)
        return response2.json()

    def write_value2(self):
        payload_write2 = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata",\
                        "data": {"newvalue": "00"}}
        response3 = requests.post(url='http://192.168.0.4', data=json.dumps(payload_write2), headers=None)
        response3.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        responses3 = response3.json()
        return response3.json()

myobj = Iolink()
myobj2=myobj.read_value()
# print(myobj2)
data = myobj2["data"]
serial =[]
for i in range(8):
    x= i+1
    serials= "/iolinkmaster/port[%i]/iolinkdevice/serial"%x
    serial.append(serials)

port_serials = []
for x in serial:
    pass
print(data)


# print(data)
# this_data =
# time.sleep(6)
# myobj.write_value()
# time.sleep(6)
# myobj.write_value2()
# time.sleep(6)
# myobj = Iolink.read_value()
# write_value()
