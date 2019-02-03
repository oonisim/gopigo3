#!/usr/bin/env python
#--------------------------------------------------------------------------------
# Handle commands from AWS IoT MQTT broker.
#--------------------------------------------------------------------------------
import easygopigo3
import easysensors
import paho.mqtt.client as mqtt
import sys, time, ssl, threading, os, string
from os.path import expanduser

PI = easygopigo3.EasyGoPiGo3()

#--------------------------------------------------------------------------------
# Environment variables
#--------------------------------------------------------------------------------
# AWS IoT MQTT broker
MQTT_HOST = os.environ['AWSIOT_MQTT_HOST']
MQTT_PORT = os.environ['AWSIOT_MQTT_PORT']
MQTT_TOPIC_COMMAND = os.environ['AWSIOT_MQTT_TOPIC_COMMAND']
MQTT_TOPIC_REPORT = os.environ['AWSIOT_MQTT_TOPIC_REPORT']
# TLS client certificate authetication
TLS_DIR = os.environ['AWSIOT_TLS_DIR']
TLS_CA_FILE = os.environ['AWSIOT_CA_FILE']
TLS_KEY_FILE = os.environ['AWSIOT_KEY_FILE']
TLS_CERT_FILE = os.environ['AWSIOT_CERT_FILE']

#--------------------------------------------------------------------------------
# GoPiGo
#--------------------------------------------------------------------------------
def servo():
    for i in range(1250, 1751):    # count from 1000 to 2000
        PI.set_servo(PI.SERVO_1, i)
        time.sleep(0.005)
    for i in range(1250, 1751):    # count from 1000 to 2000
        PI.set_servo(PI.SERVO_1, 3000-i)
        time.sleep(0.005)

    time.sleep(1)
    PI.set_servo(PI.SERVO_1, 1500)


def execute(command):
    print("execute: command is [{0}]".format(command))
    global PI
    commands = {
        "f" : PI.forward,
        "b" : PI.backward,
        "r" : PI.right,
        "l" : PI.left,
        "s" : PI.stop,
    }
    try:
        commands[command]()
        time.sleep(1)
        PI.stop()
    except:
        if command == "exit": sys.exit()
        print("Illegal command [" + command + "]")


def set_client(client):
    client.tls_set(
        ca_certs=os.path.join(TLS_DIR, TLS_CA_FILE),
        certfile=os.path.join(TLS_DIR, TLS_CERT_FILE),
        keyfile=os.path.join(TLS_DIR, TLS_KEY_FILE)
    )
    client.tls_insecure_set(False)

    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message

    setattr(get_client, "client", client)

def get_client():
    """MQTT resource accessor

    Returns:
        MQTT client
    """
    if not hasattr(get_client, "client"):
        #--------------------------------------------------------------------------------
        # MQTT Broker (AWS IoT)
        #--------------------------------------------------------------------------------
        client = mqtt.Client(
            client_id="GoPiGo3",
            clean_session=True
        )
        client.connected_flag=False

        #--------------------------------------------------------------------------------
        # The connected_flag is to test the connection and set to True by the on_connect.
        # Set to False by the on_disconnect callback function.
        # Create the flag as part of the Client Class so that available in each get_client().
        #--------------------------------------------------------------------------------
        set_client(client)

    return getattr(get_client, "client")

#--------------------------------------------------------------------------------
# Callbacks
#--------------------------------------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("on_connect: result code "+str(rc))
    #--------------------------------------------------------------------------------
    # To ensure any messages published while disconnected will be delivered once
    # the connection is restored.
    # - Set a client_id so it's the same across reconnects
    # - Set the clean_session=false connection option
    # - Subscribe at QOS greater than 0
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #--------------------------------------------------------------------------------
    print("subscribe to topic")
    #get_client().subscribe(MQTT_TOPIC_COMMAND)
    client.subscribe(MQTT_TOPIC_COMMAND, qos=1)
    client.connected_flag=True
    set_client(client)

    print("verify connect flag [{0}]".format(str(get_client().connected_flag)))
    if get_client().connected_flag is not True:
        print("connected flag not set!!!")

 
def on_disconnect(client, userdata, flags, rc=0):
    print("on_disconnect: result code [" + str(rc) + "[ client_id [" + "]")
    set_client(client)
    if get_client().connected_flag is True:
        get_client().connected_flag = False
    else:
        print("on_disconnect called while get_client().connected_flag == False")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    execute(str(msg.payload))

def connect():
    global MQTT_HOST
    global MQTT_PORT

    print("connecting")
    try:
        get_client().connect(
            host=MQTT_HOST,
            port=MQTT_PORT,
            keepalive=60,
            bind_address=""
        )
    except:
        print("connection failed. Will retry during the main loop...")

def main():
    #--------------------------------------------------------------------------------
    # Connect before loop to avoid issues.
    #--------------------------------------------------------------------------------
    connect()

    #--------------------------------------------------------------------------------
    # Start loop to process received messages
    # There is a time delay between the connection creation and the callback trigger.
    # Important to wait until the connection has been established.
    # Check AFTER start loop to make sure on_connect gets called.
    #--------------------------------------------------------------------------------
    print("client connected flag before loop_start is " + str(get_client().connected_flag))
    print("waiting for the connection to be established...")
    get_client().loop_forever()
    """
    get_client().loop_start()
    while get_client().connected_flag is False:
        time.sleep(3)
        print("Still waiting to connect...")
        #connect()

    print("Connection established")
    #--------------------------------------------------------------------------------
    # Reconnect when disconnected
    #--------------------------------------------------------------------------------
    try:
        while True:
            print("client connected flag in loop is " + str(get_client().connected_flag))
            print("sleeping")
            time.sleep(1)
            if get_client().connected_flag is False:
                print("Disconnected. Try to reconnect...")
                get_client().reconnect()

    except KeyboardInterrupt:
        print "exiting"
        get_client().disconnect()
        get_client().loop_stop()
    """


if __name__ == '__main__':
    main()
