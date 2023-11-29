import requests


def send(payload):
    # Define the URL of your Django server endpoint
    url = 'http://localhost:8000/web/MqttMiddleware/dido/'
    headers = {'Content-type': 'application/json'}
    print("here")
    if payload != "F":
        try:
            response = requests.post(url=url, json=payload, headers=headers)
            response.raise_for_status()
            # Handle successful request
            print(f"Data sent to Django server with status code: {response.status_code}")
        except:
            # Handle exceptions for the HTTP request here
            print("Failed to send data to Django server")
    else:
        pass
    
send("tst")