#!C:/python36/python.exe
#!/usr/bin/env python3
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope

#This is functioning as a server and will be responing to multiple clients
import asyncio
import os
import signal
import time

from gmqtt import Client as MQTTClient
from gmqtt.mqtt.constants import MQTTv311
# gmqtt also compatibility with uvloop  
#import uvloop
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
client_id="testclient"
mqttv=MQTTv311
messages=[]
STOP = asyncio.Event()

def on_publish(client,rc, userdata, mid):
    print("published")

def on_connect(client, flags, rc, properties):
    print('Connected ',flags)
    print('Connected ',properties)



def on_message(client, topic, payload, qos, properties):
    print('MSG Properties:', properties)
    msg=str(payload.decode("utf-8"))
    messages.append(msg)
    print('RECV MSG:', msg)
    response_topic = properties["response_topic"][0]
    print('Responding on response topic:', response_topic)
    #respond
    client.publish(response_topic,"server response message")
    
    
    


def on_disconnect(client, packet, exc=None):
    print('Disconnected ',packet)

def on_subscribe(client, mid, qos):
    print('SUBSCRIBED')

def ask_exit(*args):
    STOP.set()
async def wait(s):
    await asyncio.sleep(s)
    return True
    


async def main(broker_host):
    print("creating server")

    client = MQTTClient("server")


    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish

    await client.connect(broker_host)
    client.subscribe('org/common',no_local=True)
    
    await asyncio.sleep(5)

    print("subscribed to common topic")


    await asyncio.sleep(500) #wait to receive message


    await client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    host = '192.168.1.61'


    loop.run_until_complete(main(host))
