#!/usr/bin/env python
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time, ssl, datetime, calendar
from os.path import expanduser
 
home = expanduser("~")
dir = home + "/.ssh"
 
hostname="a2jh9d7vp4nbkx.iot.ap-southeast-2.amazonaws.com"
port=8883
tls={
    'ca_certs':dir+"/ca.pem",
    'certfile':dir+"/e48b59a7a9-certificate.pem",
    'keyfile' :dir+"/e48b59a7a9-private.pem.key"
}
topic = "/gopigo/report"
append="|0.436|TCP|112.10.20.10/0|112.10.20.10|40|172.30.190.10/0|172.30.190.10|80|43|260|1|0|0" 
while True:

    message = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d:%H:%M:%S') + append
    try:
        print("Sending message...")
        publish.single(
            topic,
            payload=message,
            qos=0,
            retain=False,
            hostname=hostname,
            port=port,
            client_id="gopigo",
            keepalive=60,
            will=None,
            auth=None,
            tls=tls,
            protocol=mqtt.MQTTv311,
            transport="tcp"
        )
        
        time.sleep(.5)
    except KeyboardInterrupt:
        print "exiting"
        client.disconnect()
        client.loop_stop() 


