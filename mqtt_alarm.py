#!/usr/bin/python

import private as priv
import RPi.GPIO as GPIO
import logging
import paho.mqtt.publish as publish
from time import sleep
from systemd.journal import JournalHandler

log = logging.getLogger('mqtt_alarm')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

MQTT_HOST = "10.100.30.6"
MQTT_TOPIC_PREFIX = "homeassistant/garagedoor/"
MQTT_CLIENT_ID = "garagepi"
MQTT_PAYLOADS = {
  0: "off",
  1: "on",
}

# Dictionary of GPIO PIN to mqtt topic
PIN_MAP = {
  7: "7",
  11: "11",
  12: "12",
  13: "13",
  16: "16",
  18: "18",
  22: "22",
  29: "29",
  32: "32",
  35: "35",
}

GPIO.setmode(GPIO.BOARD)

def state_change_hadler(channel):
  state = GPIO.input(channel)

  if state:
    log.info("Rising edge detected on {}".format(channel))
    print("Rising edge detected on {}".format(channel))
  else:
    log.info("Falling edge detected on {}".format(channel))
    print("Falling edge detected on {}".format(channel))

  publish_event(channel, state)

def publish_event(pin, state):
  topic = MQTT_TOPIC_PREFIX + PIN_MAP[pin]
  payload = MQTT_PAYLOADS[state]

  publish.single(topic, payload, hostname=MQTT_HOST, retain=True, qos=1, auth = {'username':"homeassistant", 'password':priv.password})

  log.info("Published event, topic={}, payload={}, hostname={}".format(topic, payload, MQTT_HOST))
  print ("Published event, topic={}, payload={}, hostname={}".format(topic, payload, MQTT_HOST))

for pin, name in PIN_MAP.items():
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(pin, GPIO.BOTH, callback=state_change_hadler, bouncetime=100)

  state = GPIO.input(pin)

  log.info("Mapped pin {:0>2d} to {}".format(pin, name))
  log.info("... state {}".format(state))

  publish_event(pin, state)

try:
  while True:
    sleep(60)
except KeyboardInterrupt:
  log.info("Stopping...")
finally:
  GPIO.cleanup()
