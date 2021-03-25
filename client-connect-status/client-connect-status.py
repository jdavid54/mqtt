#! c:\python34\python.exe
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
"""
Client Connection status demo code
"""
import paho.mqtt.client as mqtt  #import the client
import time,sys,random
keep_alive=60
QOS1=1
QOS2=0
CLEAN_SESSION=False
port=1883
broker="192.168.1.157"
#broker="iot.eclipse.org" #use cloud broker
cname="sensor1"
connection_status_topic="sensors/connected/"+cname
def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)
    print(m)
    client.connected_flag=False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        client.connected_flag=True #Flag to indicate success
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True
def on_log(client, userdata, level, buf):
    print("log: ",buf)
def on_message(client, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))


mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #





client = mqtt.Client("cname")    #create new instance
#client.on_log=on_log #client logging
client.on_connect=on_connect        #attach function to callback
client.on_disconnect=on_disconnect
print("publising on ",connection_status_topic )
print("Setting will message")
client.will_set(connection_status_topic,"False",0,True) #set will message
print("connecting ",broker)
client.connect(broker,port,keep_alive)
while not client.connected_flag:
    client.loop()
    time.sleep(1)#wait for connection

client.publish(connection_status_topic,"True",0,True)#use retain flag

time.sleep(60)
print("updating status and disconnecting")
client.publish(connection_status_topic,"False",0,True)
client.disconnect()

