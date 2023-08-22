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
    port_1 = "/iolinkmaster/port[1]/iolinkdevice/pdin/"
    port_2 = "/iolinkmaster/port[2]/iolinkdevice/pdin/"
    port_3 = "/iolinkmaster/port[3]/iolinkdevice/pdin/"
    port_4 = "/iolinkmaster/port[4]/iolinkdevice/pdin/"
    port_5 = "/iolinkmaster/port[5]/iolinkdevice/pdin//"
    port_6 = "/iolinkmaster/port[6]/iolinkdevice/pdin/"
    port_7 = "/iolinkmaster/port[7]/iolinkdevice/pdin/"
    port_8 = "/iolinkmaster/port[8]/iolinkdevice/pdout/"
    payload_read = {"code": "request", "cid": 4711, "adr": "/getdatamulti", \
                        "data": {
                            "datatosend": [serial_1, port_1, serial_2, port_2, serial_3, port_3, serial_4, port_4,serial_5, \
                                port_5, serial_6, port_6, serial_7, port_7, serial_8,port_8]}}
    payload_write = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "01"}}
    payload_write2 = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "00"}}
    
    def read_value(self):

        payload_read = {"code": "request", "cid": 4711, "adr": "/getdatamulti", \
                        "data": { \
                            "datatosend": [self.serial_1, self.port_1, self.serial_2, self.port_2, self.serial_3,
                                           self.port_3, self.serial_4, self.port_4,
                                           self.serial_5, self.port_5, \
                                           self.serial_6, self.port_6, self.serial_7, self.port_7, self.serial_8,
                                           self.port_8]
                        }
                        }
        headers = {}
        headers['Content-Type'] = 'application/json'

        try:
            response = requests.post(url='http://192.168.0.4', data=json.dumps(payload_read), headers=None)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            responses = response.json()
            print(response)
            print(responses)
            pretty_json = json.dumps(responses, indent=4)
            print(pretty_json)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def write_value(self):
        payload_write = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata",
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
        payload_write2 = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata",
                          "data": {"newvalue": "00"}}
        response3 = requests.post(url='http://192.168.0.4', data=json.dumps(payload_write2), headers=None)
        response3.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        responses3 = response3.json()
        return response3.json()

myobj = Iolink()
# myobj.read_value()
# myobj.write_value()
myobj.write_value2()
# myobj = Iolink.read_value()
# time.sleep(1)
# write_value()
