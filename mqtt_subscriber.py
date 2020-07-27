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
MQTT_TOPIC_PREFIX = "garagedoor/door-up"
MQTT_TOPIC_PREFIX2 = "garagedoor/door-down"
MQTT_CLIENT_ID = "garagepi"

GPIO.setmode(GPIO.BOARD)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code {0}".format(str(rc)))
  client.subscribe(MQTT_TOPIC_PREFIX)
  client.subscribe(MQTT_TOPIC_PREFIX2)

def on_message(client, userdata, msg):
  print("Message received-> " + msg.topic + " " + str(msg.payload))
  if 'door-open' in msg.topic:
    print 'door Open match - enable GPIO Here'

def subscribe_topic():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(username=priv.username, password=priv.password)
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
