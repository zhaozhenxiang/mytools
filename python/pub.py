import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
# client.on_message = on_message

client.connect("ir.api.everyoo.com", 1883, 60)
# client.connect("smarthomemqtest.api.everyoo.com", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()

client.loop_start()
import time
i = 1
while i < 1000:
    client.publish("/everyoo/gateway/toserver", "f0fe6b4c0206,env,2925,5051")
    
    # client.publish("/everyoo/gateway/toserver", "f0fe6b4c0206asdas,env,2925,5051")
    i += 1
    # time.sleep(0.3)
