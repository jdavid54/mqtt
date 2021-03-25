#! python3.4
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
demo connect and reconnect scipt
"""
import paho.mqtt.client as mqtt
import time
import logging
import sys

def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")
    if rc==0:
        client.connected_flag=True
        #client.subscribe("house/bulb1")
    else:
        client.bad_connection_flag=True
def on_disconnect(client, userdata,flags, rc=0):
    print("DisConnected flags"+"result code "+str(rc))
    client.connected_flag=False
def Connect(client,broker,port,keepalive):
    connflag=False
    print("connecting ",broker)
    badcount=0 # counter for bad connection attempts
    while not connflag:
        logging.info("connecting to broker "+str(broker))
        try:
            res=client.connect(broker,port,keepalive)      #connect to broker
            if res==0:
                connflag=True
                return 0
            else:
                logging.debug("connection failed ",res)
                badcount +=1
                if badcount==3:
                    return -1
                    raise SystemExit #give up

        except:
            client.badconnection_flag=True
            logging.debug("connection failed")
            badcount +=1
            if badcount==3:
                return -1
                raise SystemExit #give up
    return 0
    #####end connecting

def wait_for(client,msgType,period=1,wait_time=10):
    wcount=0  
    while True:
        logging.info("waiting"+ msgType)
        if msgType=="CONNACK":
            if client.on_connect:
                if client.connected_flag:
                    return True
                if client.bad_connection_flag: #
                    return False
                
        if msgType=="SUBACK":
            if client.on_subscribe:
                if client.suback_flag:
                    return True
        if msgType=="MESSAGE":
            if client.on_message:
              return True
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True
###########
loglevel="DEBUG"
logging.basicConfig(level=loglevel) #error logging
#use DEBUG,INFO,WARNING,ERROR
client=mqtt.Client("P11")
###set flags in client object
mqtt.Client.bad_connection_flag=False
mqtt.Client.connected_flag=False
mqtt.Client.disconnect_flag=False
####
broker="192.168.1.85" #need to change this
port=1883
keepalive=60
client.loop_start
###set callbacks
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.running_loop=False #needed by wait_for loop
run_flag=True
client.loop_start() #start a loop
if not client.connected_flag: #flag set in on_connect callback
    if Connect(client,broker,port,keepalive) !=-1: 
        if not wait_for(client,"CONNACK"): 
            run_flag=False #need to take action to quit
    else:
        run_flag=False #need to take action to quit
count=0
retry_count=0
while run_flag:
    if client.connected_flag:#check for connection
        print("in loop would pub and sub here",count)
        count+=1
    else:
        retry_count+=1
        if retry_count>=3:
            run_flag=False #break from loop
    time.sleep(2)
client.loop_stop()
client.disconnect()

