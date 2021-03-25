import paho.mqtt.client as paho
import time
broker="192.168.1.61"
from queue import Queue
Q = Queue()
port=1883
topic1 ="Flights/Air France/#"
flights={}

def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   msg=str(message.payload.decode("utf-8"))
   m="[Flight "+  message.topic.split('/')[-1] +"] "+ msg
   if message.topic in flights:
      if flights[message.topic]==msg:
         print("Not changed ",message.topic)
      else:
         flights[message.topic]=msg
         Q.put(m)
   else:
      flights[message.topic]=msg


def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos," ",mid, "\n")
   pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)


client= paho.Client("Python2",False)       #create client object
#client.on_log=on_log #this gives getailed logging
client.on_subscribe = on_subscribe   #assign function to callback
client.on_disconnect = on_disconnect #assign function to callback
client.on_connect = on_connect #assign function to callback
client.on_message=on_message
print("connecting to broker ",broker)
client.connect(broker,port)           #establish connection
time.sleep(1)
time.sleep(2)
print("Subscribing to topics ",topic1)
r=client.subscribe(topic1,0)    #subscribe single topic
tstart=time.time()
while True: #runs forever break with CTRL+C
   client.loop(.001)
   if time.time()-tstart>=3:
      while not Q.empty():
         m=Q.get()
         print(m)
      #print("*****************")
      tstart=time.time()
   
   #time.sleep(1)
   
client1.disconnect()

