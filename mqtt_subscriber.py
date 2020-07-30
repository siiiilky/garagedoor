#!/usr/bin/python

# Steven Coutts - stevec@couttsnet.com
#
# 29/07/2020
# Script to subscribe to a few MQTT topics on Home Assistant
# Do stuff based on received messages.
# Beginnings of LCD control functionality.
#

import private as priv
import lcd as lcd
import RPi.GPIO as GPIO
import logging
import paho.mqtt.client as mqtt
from time import sleep
from systemd.journal import JournalHandler
from datetime import datetime
import socket

log = logging.getLogger('mqtt_alarm')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

GPIO.setmode(GPIO.BCM)
GPIO.setup(priv.pindown, GPIO.OUT)
GPIO.setup(priv.pinup, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code {0}".format(str(rc)))
  client.subscribe(priv.MQTT_TOPIC_PREFIX)
  client.subscribe(priv.MQTT_TOPIC_PREFIX2)
  client.subscribe(priv.MQTT_TOPIC_PREFIX_ALARM)
  client.subscribe(priv.MQTT_TOPIC_PREFIX_GARAGE)

def on_message(client, userdata, msg):
  print("Message received-> " + msg.topic + " " + str(msg.payload))
  log.info("Message received-> " + msg.topic + " " + str(msg.payload))
  if 'door-up' in msg.topic:
    if 'off' in msg.payload:
      GPIO.output(priv.pinup, 1)
    elif 'on' in msg.payload:
      GPIO.output(priv.pinup, 0)
  elif 'door-down' in msg.topic:
    if 'off' in msg.payload:
      GPIO.output(priv.pindown, 1)
    elif 'on' in msg.payload:
      GPIO.output(priv.pindown, 0)
  elif 'alarm' in msg.topic:
    if 'off' in msg.payload:
      lcd.lcd_string("Alarm DISARMED", lcd.LCD_LINE_2)
    elif 'on' in msg.payload:
      lcd.lcd_string("Alarm ARMED", lcd.LCD_LINE_2)
  elif 'garagesensor' in msg.topic:
    if 'off' in msg.payload:
      lcd.lcd_string("Garage Door OPEN", lcd.LCD_LINE_3)
    elif 'on' in msg.payload:
      lcd.lcd_string("Garage Door CLOSED", lcd.LCD_LINE_3)

def subscribe_topic():
  # Initialise display
  lcd.lcd_init()
  lcd.lcd_string("IP " + IPAddr, lcd.LCD_LINE_1)
  lcd.lcd_string("Alarm UNKNOWN", lcd.LCD_LINE_2)
  lcd.lcd_string("Garage Door UNKNOWN", lcd.LCD_LINE_3)
  lcd.lcd_string("Someone is HOME", lcd.LCD_LINE_4)
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(username=priv.username, password=priv.password)
  client.connect(priv.MQTT_HOST, 1883)
  client.loop_forever()

try:
  subscribe_topic()
except KeyboardInterrupt:
  log.info("Stopping...")
finally:
  print "*** GPIO Cleanup ***"
  GPIO.cleanup()
  lcd.lcd_byte(0x01, lcd.LCD_CMD)
