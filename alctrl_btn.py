import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import socket
from gpiozero import Button, LED, MotionSensor
from time import sleep
from datetime import datetime
from signal import pause

# Get the current hostname of this client.
CLIENT_ID = socket.gethostname()
IP_ADDR = socket.gethostbyname(CLIENT_ID)

button = Button(18)
orange_lamp = LED(27)
red_lamp = LED(17)
server = "172.25.24.60"
port = 8883
topic = "buhler/buz/dlc/andon_light/buz0ait00014/events"
ctrl_topic = "buhler/buz/dlc/andon_light/buz0ait00014/ctrl"
epoch = datetime(1970,1,1,0,0,0)
start = datetime.utcnow()
end = None
code = 0
pressed = False


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(ctrl_topic)


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(server, port, 60)
except:
    print("Failed to connect to mqtt broker")


def init_gpio():
    """
    Initialize gpio controller and configure input output pins.
    :return:
    """

    orange_lamp.on()
    red_lamp.off()
    sleep(0.2)
    orange_lamp.off()
    red_lamp.on()
    sleep(0.2)
    orange_lamp.on()
    red_lamp.off()
    sleep(0.2)
    orange_lamp.off()
    red_lamp.on()
    sleep(0.2)
    red_lamp.off()


def normal():
    orange_lamp.off()
    red_lamp.off()


def issue():
    orange_lamp.on()
    red_lamp.off()


def alert():
    orange_lamp.off()
    red_lamp.on()


def switch_code():
    global code
    if code == 0:
        print("Issue")
        code = 1
        issue()
    elif code == 1:
        print("Alert")
        alert()
        code = 2
    elif code == 2:
        print("Normal")
        normal()
        code = 0


button.when_pressed = switch_code

init_gpio()
pause()
