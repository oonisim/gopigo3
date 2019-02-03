#!/usr/bin/env bash
export AWSIOT_MQTT_HOST='aix88q3urwa6k.iot.us-east-1.amazonaws.com'
export AWSIOT_MQTT_PORT=8883
export AWSIOT_MQTT_TOPIC_COMMAND="/gopigo/command"
export AWSIOT_MQTT_TOPIC_REPORT="/gopigo/report"
export AWSIOT_TLS_DIR="$(realpath ~pi)/.ssh"
export AWSIOT_CA_FILE="ca_aws_iot.pem"
export AWSIOT_KEY_FILE="iot.key.nonencrypted"
export AWSIOT_CERT_FILE="iot.crt"

(cd ${AWSIOT_TLS_DIR} && echo "Q" | openssl s_client -connect ${AWSIOT_MQTT_HOST}:${AWSIOT_MQTT_PORT} -CAfile ${AWSIOT_CA_FILE} -cert ${AWSIOT_CERT_FILE} -key ${AWSIOT_KEY_FILE})
