import requests
import json

# Define the URL and JSON payload
url = "http://iolink-master-device/api"
payload = {
    "key1": "value1",
    "key2": "value2"
}

# Convert payload to JSON string
json_payload = json.dumps(payload)

# Set headers and send the POST request
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json_payload, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Get the response data
    response_data = response.json()
    print(response_data)
else:
    print("Error:", response.status_code)