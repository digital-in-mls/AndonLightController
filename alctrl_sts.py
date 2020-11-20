from gpiozero import LED, MotionSensor
import paho.mqtt.client as mqtt
from time import sleep
import json
from datetime import datetime

green_lamp = LED(22)
orange_lamp = LED(27)
red_lamp = LED(17)
pir = MotionSensor(24)

server = "172.25.24.60"
port = 8883
topic = "buhler/buz/dlc/andon_light/buz0ait00014/status"
epoch = datetime(1970,1,1,0,0,0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(server, port, 60)
except:
    print("Failed to connect to mqtt broker")

client.loop_start()
while 1:
    start = datetime.now()
    ts = (start - epoch).total_seconds()

    pl = json.dumps(
        {
            'gpio_values': {
                'pir': int(pir.value),
                'green_led': int(green_lamp.value),
                'orange_led': int(orange_lamp.value),
                'red_led': int(red_lamp.value)
            },
            'andon_status': {
                'is_active': True if green_lamp.value == 1 else False,
                'is_issue': True if orange_lamp.value == 1 else False,
                'is_alert': True if red_lamp.value == 1 else False,
                'is_breakdown': True if orange_lamp.value == 1 and red_lamp.value == 1 else False
            }
        }
    )

    try:
        client.publish(topic, pl)
    finally:
        print("Payload dispatched: " + pl)
    sleep(1)
