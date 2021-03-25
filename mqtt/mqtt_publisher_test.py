import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    print("CTRL-Z to stop")
    
client = mqtt.Client()
print(client)
client.on_connect = on_connect

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
brokers = ["test.mosquitto.org","broker.emqx.io","192.168.1.100","192.168.1.100","77.134.40.243"]
broker_id = -1
broker = brokers[broker_id]
#client.connect("test.mosquitto.org", 1883, 60)
#client.connect("broker.emqx.io", 1883, 60)
status = client.connect(broker, 1883, 60)
print(status)
# send a message to the raspberry/topic every 1 second, 5 times in a row
for i in range(5):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    msg = "hello "+str(i) +" from thonny"
    client.publish('raspberry/topic', payload=msg, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)
client.loop_forever()