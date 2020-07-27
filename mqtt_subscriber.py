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
  if 'door-up' in msg.topic:
    if 'off' in msg.payload:
      print 'Door up Turn Off - enable GPIO Here'
      GPIO.setup(priv.pinup, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      GPIO.add_event_detect(priv.pinup, GPIO.BOTH, callback=state_change_hadler, bouncetime=100)
      state = GPIO.input(priv.pinup)
      log.info("Mapped pin {:0>2d} to {}".format(pin, name))
      log.info("... state {}".format(state))
    elif 'on' in msg.payload:
      print 'Door up Turn On - enable GPIO Here'
      GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(priv.pinup, GPIO.BOTH, callback=state_change_hadler, bouncetime=100)
      state = GPIO.input(priv.pinup)
      log.info("Mapped pin {:0>2d} to {}".format(pin, name))
      log.info("... state {}".format(state))
  elif 'door-down' in msg.topic:
    if 'off' in msg.payload:
      print 'Door down Turn Off - enable GPIO Here'
      GPIO.setup(priv.pindown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(priv.pindown, GPIO.BOTH, callback=state_change_hadler, bouncetime=100)
      state = GPIO.input(priv.pindown)
      log.info("Mapped pin {:0>2d} to {}".format(pin, name))
      log.info("... state {}".format(state))
    elif 'on' in msg.payload:
      print 'Door down Turn On - enable GPIO Here'
      GPIO.setup(priv.pindown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(priv.pindown, GPIO.BOTH, callback=state_change_hadler, bouncetime=100)
      state = GPIO.input(priv.pindown)
      log.info("Mapped pin {:0>2d} to {}".format(pin, name))
      log.info("... state {}".format(state))

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
