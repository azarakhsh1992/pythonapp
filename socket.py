import socket
import json

# Define the target server and port
server = 'example.com'
port = 80

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server, port))

# Create the JSON object
data = {
    "key1": "value1",
    "key2": "value2"
}
json_data = json.dumps(data)

# Send the POST request
request = "POST /path/to/endpoint HTTP/1.1\r\nHost: {0}\r\nContent-Type: application/json\r\nContent-Length: {1}\r\n\r\n{2}".format(server, len(json_data), json_data)
client_socket.sendall(request.encode())

# Receive the response
response = b""
while True:
    data = client_socket.recv(4096)
    if not data:
        break
    response += data

# Print the response
print(response.decode())

# Close the socket
client_socket.close()