import asyncio
import websockets
import json
import socket
import sockets
import sys
from containerprog import Iolink

myobj = Iolink()

ip = myobj.url
port = 800

# Create the JSON object
data = myobj.payload_read
data2= myobj.payload_write
data3 = myobj.payload_write2

json_data = json.dumps(data)
client_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ip)
client_socket.send(json_data.encode())
client_socket.close()
