import time
import json
from azure.iot.device import IoTHubDeviceClient, Message
import random as r

def get_temp():
    return r.randint(16,25)

def get_humidity():
    return r.randint(1,120)

def get_people():
    return r.randint(0,580)

def get_memory():
    return r.randint(1,100)

def get_cpu():
    return r.randint(1,100)

connection_string = ""
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
print('Connecting')
device_client.connect()
print('Connected')


def simulate_messages():

    message = Message(json.dumps({
    "nPeople": get_people(),
    "CPU": get_cpu(),
    "Humidity": get_humidity(),
    "Memory": get_memory(),
    "Temperature": get_temp()
    }
    ))

    return message

while True:

    message = simulate_messages()

    device_client.send_message(message)
    print(f"Simulated message: {message}")
    print("Simulated data: sent")

    time.sleep(10)
