#!/usr/bin/python

import private as priv
import RPi.GPIO as GPIO
import logging
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from time import sleep
from systemd.journal import JournalHandler

log = logging.getLogger('mqtt_alarm')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

MQTT_HOST = "10.100.30.6"
MQTT_TOPIC_PREFIX = "garagedoor/"
MQTT_CLIENT_ID = "garagepi"

GPIO.setmode(GPIO.BOARD)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code {0}".format(str(rc)))
  client.subscribe(MQQT_TOPIC_PREFIX)

def on_message(client, userdata, msg):
  print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

def subscribe_topic():

  client = mqtt.Client("ha-mqqt")
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(username="homeassistant", password=priv.password)
  client.connect(MQTT_HOST, 1883)
  client.loop_forever()  # Start networking daemon

subscribe_topic()

try:
  while True:
    sleep(60)
except KeyboardInterrupt:
  log.info("Stopping...")
finally:
  GPIO.cleanup()
