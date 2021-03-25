###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
Client Connection demo code
"""
import paho.mqtt.client as mqtt  #import the client
import time,sys
keep_alive=60
def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)+"client_id  "
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
QOS1=1
QOS2=0
CLEAN_SESSION=False
port=1883
broker="192.168.1.61"
#broker="iot.eclipse.org" #use cloud broker
client = mqtt.Client("P!")    #create new instance
#client.on_log=on_log #client logging
mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #
client.on_connect=on_connect        #attach function to callback
client.on_disconnect=on_disconnect
run_main=False
run_flag=True
while run_flag:
    while not client.connected_flag and client.retry_count<3:
        count=0 
        run_main=False
        try:
            print("connecting ",broker)
            client.connect(broker,port,keep_alive)      #connect to broker
            break #break from while loop
        except:
            print("connection attempt failed will retry")
            client.retry_count+=1
            if client.retry_count>3:
                run_flag=False
    if not run_main:   
        client.loop_start()
        while True:
            if client.connected_flag: #wait for connack
                client.retry_count=0 #reset counter
                run_main=True
                break
            if count>6 or client.bad_connection_flag: #don't wait forever
                client.loop_stop() #stop loop
                client.retry_count+=1
                if client.retry_count>3:
                    run_flag=False
                break #break from while loop

            time.sleep(1)
            count+=1
    if run_main:
        try:
            #Do main loop
            print("in main loop")#publish and subscribe here
            time.sleep(3)
            ##Added try block to catch keyborad interrupt  to break loop so we
            ##don't leave loop thread running.

        except(KeyboardInterrupt):
            print("keyboard Interrupt so ending")
            run_flag=False

print("quitting")
client.disconnect()
client.loop_stop()
