#! c:\python34\python.exe
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope

import paho.mqtt.client as mqtt  #import the client
import time

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print(" \n In on_connect callback ")
    loop_flag=0

broker_address="192.168.1.157"
#broker_address="iot.eclipse.org"
client = mqtt.Client()     #create new instance
client.on_connect=on_connect        #attach function to callback
client.connect(broker_address)      #connect to broker
##comment out so callback fails
#client.loop_start()        #start loop to process callbacks

loop_flag=1
counter=0
while loop_flag==1:
    print("waiting for callback to occur ",counter)
    time.sleep(.5)  #pause 1/2 second
    counter+=1
    if counter >50: #taking too long quit
        print("Taking too long quitting")
        break


client.disconnect()
client.loop_stop()


#client.on_subscribe=on_subscribe        #attach function to callback
#r=client.subscribe("bulbs/#")
#print("subscribe result ", r)
def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
    global loop_flag
    print("In on subscribe callback")
    loop_flag=0
