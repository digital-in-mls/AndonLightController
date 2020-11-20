'''
Andon Light Controller Single Shot Script
This script send a message on every change by motion detection sensor to the mqtt broker.
'''

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import socket
from gpiozero import Button, LED, MotionSensor
from time import sleep
from datetime import datetime

# Get the current hostname of this client.
CLIENT_ID = socket.gethostname()
IP_ADDR = socket.gethostbyname(CLIENT_ID)

pir = MotionSensor(24)
green_lamp = LED(22)
server = "172.25.24.60"
port = 8883
topic = "buhler/buz/dlc/andon_light/buz0ait00014/activity"
epoch = datetime(1970,1,1,0,0,0)
start = None
end = None

def init_gpio():
    """
    Initialize gpio controller and configure input output pins.
    :return:
    """

    green_lamp.on()
    sleep(0.1)
    green_lamp.off()
    sleep(0.3)
    green_lamp.on()
    sleep(0.1)
    green_lamp.off()
    sleep(0.3)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(server, port, 60)
except:
    print("Failed to connect to mqtt broker")

init_gpio()

client.loop_start()
while 1:
    if pir.motion_detected:
        print("Motion detected")
        green_lamp.on()

        start = datetime.now()
        ts_start = (start - epoch).total_seconds()

        while pir.value == 1:
            sleep(60)

        print("No Motion detected")

        end = datetime.now()
        ts_end = (end - epoch).total_seconds()
        duration = ts_end - ts_start
        pl = json.dumps(
            {
                'building': 'H8105',
                'assembly_line': "VSC",
                'workplace_id': 1,
                'event': "activity",
                'event_id': 1,
                'timestamp': int(ts_start),
                'ts_start': int(ts_start),
                'ts_end': int(ts_end),
                'duration': int(ts_end - ts_start)
            }
        )

        print("Sending message...")
        print("Payload: " + pl)

        try:
            client.publish(topic, pl)
        finally:
            print("Message sent!")

        green_lamp.off()
