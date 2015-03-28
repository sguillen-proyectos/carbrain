#!/usr/bin/python

import time
import json
import utils as _
from serial import Serial
from carlog import logger
from threading import Thread
from beehive import InternetConnectionInterface
from cerebro import ManejaAuto

GPS_ENABLED = False

car = ManejaAuto()

def on_connect(client, userdata, rc):
  logger.info('connected to beehive')
  client.subscribe('car/command')

def on_message(client, userdata, msg):
  global GPS_ENABLED
  logger.info(msg.topic + " " + msg.payload)
  topic = msg.topic
  data = json.loads(msg.payload)
  if topic == 'car/command':
    command = data['cmd']
    if command == 'G':
      logger.info('Enabling GPS')
      GPS_ENABLED = True
    elif command == 'H':
      logger.info('Disabling GPS')
      GPS_ENABLED = False
    elif command == '1' or command == '2':
      logger.info('Executing Braking')
      car.activar_motor(command)
    client.publish('car/confirmation', data['time'])

s = Serial('/dev/ttyUSB3', 115200, timeout=1)

mqtt_host = 'iot.tiendamerx.com'
mqtt_port = 1883
mqtt_user = 'raspberry'
mqtt_password = 'client'

connection_interface = InternetConnectionInterface(mqtt_host, mqtt_port, mqtt_user, mqtt_password, on_connect, on_message)
class ConnectionInterfaceThread(Thread):
  def run(self):
    logger.info('Starting Connection')
    connection_interface.connect()

connection_thread = ConnectionInterfaceThread()
connection_thread.daemon = True
connection_thread.start()

logger.info('Starting...')

class GPSReader(Thread):
  def run(self):
    logger.info('Starting GPS reading...	')
    while True:
      try:
        msg = self.modem.read(1024)

        if len(msg) > 0:
          index = msg.find('+CGPSINFO:')
          if (index != -1):
            index = index + 10

            msg = msg[index:]
            index2 = msg.find('OK')
            if (index2 != -1):
              msg = msg[0:index2]

            index3 = msg.find('\r')
            if index3 != -1:
              msg = msg[0:index3]

            res = msg.split(',')
            logger.info(res)

            if GPS_ENABLED:
              logger.info('Sending to mqtt')
              position = _.get_position(res)
              data_json = json.dumps(position)
              logger.info('POSITION ' + data_json)

              connection_interface.send('location', data_json)
            else:
              logger.info('GPS not enabled')

          logger.info(msg)
        else:
          logger.info("empty message")
      except Exception as e:
        logger.error(e)

class HeartBeatThread(Thread):
  def run(self):
    while True:
      connection_interface.send('heartbeat', None)
      time.sleep(15)

def start_tracker():
  reader = GPSReader()
  reader.modem = s
  reader.daemon = True
  reader.start()

  heartbeat = HeartBeatThread()
  heartbeat.daemon = True
  heartbeat.start()

  logger.info("Configuring GPS")
  s.write('AT+CGPSURL="supl.google.com:7276"\r')
  s.write('AT+CGPSSSL=0\r')
  s.write('AT+CGPS=1,2\r')
  while True:
    s.write('AT+CGPSINFO\r')
    time.sleep(5)

'''
['1630.227844', 'S', '06807.767347', 'W', '200215', '165534.0', '3624.0', '0', '0']

'''
