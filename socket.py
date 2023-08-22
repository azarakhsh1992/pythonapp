import asyncio
import websockets
import json


async def send_json_receive_response():
    # Define the target server and port
    server = 'example.com'
    port = 80

    # Create the JSON object
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    json_data = json.dumps(data)

    # Connect to the server
    async with websockets.connect(f"ws://{server}:{port}") as websocket:
        # Send the JSON object
        await websocket.send(json_data)

        # Receive the response
        response = await websocket.recv()

        # Print the response
        print(response)

    # Close the websocket connection
    websocket.close()


# Run the function to send JSON, receive response, print it, and close the socket
asyncio.get_event_loop().run_until_complete(send_json_receive_response())
#sjlahdlasjk