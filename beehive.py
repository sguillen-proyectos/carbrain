#!/usr/bin/python

import paho.mqtt.client as mqtt
from carlog import logger
# from cerebro import ManejaAuto

# ma = ManejaAuto()

# GPS_ENABLED = False

class InternetConnectionInterface:
  def __init__(self, mqtt_host, mqtt_port, mqtt_user, mqtt_password,on_connect,on_message):
    self.client = mqtt.Client()
    self.client.on_connect = on_connect
    self.client.on_message = on_message

    self.mqtt_host = mqtt_host
    self.mqtt_port = mqtt_port
    self.mqtt_user = mqtt_user
    self.mqtt_password = mqtt_password

  def connect(self):
    print self.mqtt_host, self.mqtt_port
    self.client.connect(self.mqtt_host, self.mqtt_port, 60)
    self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
    self.client.loop_forever()

  def send(self, cmd, data):
    if cmd == 'location':
      self.__send_position(data)
    elif cmd == 'heartbeat':
      self.__send_heartbeat()
    else:
      print 'Command not found'

  def __send_position(self, data):
    data = str(data)
    self.client.publish('D286D9B8-9B66-AB85-5484-EE7DB3BE6F3A/position', data)

  def __send_heartbeat(self):
    self.client.publish('D286D9B8-9B66-AB85-5484-EE7DB3BE6F3A/heartbeat', '1')
