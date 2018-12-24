#!/usr/bin/env python
#--------------------------------------------------------------------------------
# Handle commands from AWS IoT MQTT broker.
#--------------------------------------------------------------------------------
import easygopigo3
import easysensors
import paho.mqtt.client as mqtt
import sys, time, ssl, threading
from os.path import expanduser

#--------------------------------------------------------------------------------
# GoPiGo
#--------------------------------------------------------------------------------
pi = easygopigo3.EasyGoPiGo3()
def execute(command):
    commands = {
        "forward"   : pi.forward,
        "backward" : pi.backward,
        "right"    : pi.right,
        "left"     : pi.left,
        "stop"     : pi.stop,
    }
    try:
        commands[command]()
    except:
        if (command == "exit"): sys.exit()
        print("Illegal command [" + command + "]")

    time.sleep(3)
    pi.stop()

#--------------------------------------------------------------------------------
# Locations
#--------------------------------------------------------------------------------
home = expanduser("~pi")
TLS_DIR = home + "/.ssh"

#--------------------------------------------------------------------------------
# MQTT Broker (AWS IoT)
#--------------------------------------------------------------------------------
host="MQTT broker hostname/ip"
port=8883
ca_cert     = TLS_DIR + "/" + "ca.pem"
client_cert = TLS_DIR + "/" + "e48b59a7a9-certificate.pem"
client_key  = TLS_DIR + "/" + "e48b59a7a9-private.pem.key"
tls={
    'ca_certs':ca_cert, 
    'certfile':client_cert, 
    'keyfile' :client_key
}
topic_command="/gopigo/command"
topic_report ="/gopigo/report"

#--------------------------------------------------------------------------------
# Callbacks
#--------------------------------------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #--------------------------------------------------------------------------------
    # To ensure any messages published while disconnected will be delivered once
    # the connection is restored.
    # - Set a client_id so it's the same across reconnects
    # - Set the clean_session=false connection option
    # - Subscribe at QOS greater than 0
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #--------------------------------------------------------------------------------
    print("subscribing ")
    #client.subscribe(topic_command)
    client.subscribe(topic_command, qos=1)
    # $SYS/# cause the program to stop. Why?
    #client.subscribe("$SYS/#")
    client.connected_flag=True

 
def on_disconnect(client, userdata, flags, rc=0):
    if client.connected_flag == True:
        print("DisConnected: result code [" + str(rc) + "[ client_id [" + "]")
        client.connected_flag = False
    else:
        print("on_disconnet called while client.connected_flag == False")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    execute(str(msg.payload))

def connect(client, host, port):
    print("connecting")
    try:
        client.connect(
            host=host,
            port=port,
            keepalive=60,
            bind_address=""
        )
    except:
        print("connection failed. Will retry during the main loop...")

#--------------------------------------------------------------------------------
# The connected_flag is to test the connection and set to True by the on_connect.
# Set to False by the on_disconnect callback function.
# Create the flag as part of the Client Class so that available in each client.
#--------------------------------------------------------------------------------
mqtt.Client.connected_flag=False
client = mqtt.Client(
    client_id="GoPiGo3",
    clean_session=True
)
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(
    ca_certs=ca_cert,
    certfile=client_cert,
    keyfile=client_key
)
client.tls_insecure_set(True)

#--------------------------------------------------------------------------------
# Connect before loop to avoid issues.
#--------------------------------------------------------------------------------
connect(client, host, port)

#--------------------------------------------------------------------------------
# Start loop to process received messages
# There is a time delay between the connection creation and the callback trigger.
# Important to wait until the connection has been established.
# Check AFTER start loop to make sure on_connect gets called.
#--------------------------------------------------------------------------------
print("client connected flag before loop_start is " + str(client.connected_flag))
client.loop_start()
while not client.connected_flag:
    print("wait for connection to be established...")
    time.sleep(1)
    if not client.connected_flag:
        print("Disconnected. Try to connect")
        connect(client, host, port) 

#--------------------------------------------------------------------------------
# Reconnect when disconnected
#--------------------------------------------------------------------------------
try:
    while True:
        print("client connected flag in loop is " + str(client.connected_flag))
        print("sleeping")
        time.sleep(1)
        if not client.connected_flag:
            print("Disconnected. Try to reconnect")
            client.reconnect()
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
