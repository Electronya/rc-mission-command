#!/bin/bash
# Start the broker container.

BROKER_ROOT="/home/jbacon/Documents/Electronya/RcProjects/rc-mission-commander/broker/"
BROKER_CONFIG="config"
BROKER_DATA="data"
BROKER_LOG="log"

docker run -d --rm -p 1883:1883 -p 9001:9001 \
    -v ${BROKER_ROOT}${BROKER_CONFIG}:/mosquitto/config \
    -v ${BROKER_ROOT}${BROKER_DATA}:/mosquitto/data \
    -v ${BROKER_ROOT}${BROKER_LOG}:/mosquitto/log \
    --name mission-broker eclipse-mosquitto
