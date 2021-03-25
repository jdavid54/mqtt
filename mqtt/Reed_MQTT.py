# include libraries
import paho.mqtt.client as MQTT
import RPi.GPIO as GPIO
import time

# setup
GPIO.setmode(GPIO.BCM)  # use Broadcom pin-numbering
'''
The GPIO.BOARD option specifies that you are referring to the pins by the number of the pin
the the plug - i.e the numbers printed on the board (e.g. P1) and in the middle of the
diagrams below.

The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number,
these are the numbers after "GPIO" in the green rectangles around the outside of the below
diagrams:

ex BCM 14 (GPIO14) = BOARD pin 8
'''
GPIO.setwarnings(False) # disable warnings

# configure pins
GPIO.setup(14, GPIO.OUT)  # use Broadcom pin-numbering
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pullup up inactive 

# callback after connecting to MQTT server
def on_connect(self, client, userdata, rc):
    print("Connected!")
    print("Subscribing to ToDevice/All")
    self.subscribe("ToHost/All")
    print("Subscribing to ToDevice/RaspberryPi")
    self.subscribe("ToHost/RaspberryPi")
    
# callback when publishing
def on_message(client, userdata, msg):
    print('msg:',msg.topic + " " + msg.payload.decode('utf-8'))
    global state
    if msg.payload.decode('utf-8') == "SOLVE":
        state = 1
        print('state',state)
    if msg.payload.decode('utf-8') == "RESET":
        state = 0
        print('state',state)

def on_disconnect(client,userdata, rc):
    client.loop_stop()


# Global variables
prevInput = 0
state = 0
prevState = 0

#setup MQTT
client = MQTT.Client()
# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
# connect to server
client.connect("192.168.1.100", 1883, 60)

client.loop_start()
#client.loop_forever()
print("Go main")
input = GPIO.input(4)
#print('input:',input)

# main program loop
while True:
    #print("Go main")
    # get the switch state on pin 14
    input = GPIO.input(4)
    #print(prevInput, input, state)
    if ((prevInput) and not input):
        # toggle state
        state = 1-state
        #print(state)
    prevInput = input
    
    if (prevState != state):
        #print(state)
        if (state == 0):
            #client.publish("ToHost/All", "Reed reset")
            GPIO.output(14, GPIO.HIGH)
        else:
            #client.publish("ToHost/All", "Reed solved")
            GPIO.output(14, GPIO.LOW)
    prevState = state
    #state = 1-state
    time.sleep(0.1)