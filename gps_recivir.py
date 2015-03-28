#!/usr/bin/python

from serial import Serial
from threading import *
import time
from connection import InternetConnectionInterface

s = Serial('/dev/ttyUSB3', 115200, timeout=1)
mqtt_host = 'iot.tiendamerx.com'
mqtt_port = 1883
mqtt_user = 'raspberry'
mqtt_password = 'client'

connection_interface = InternetConnectionInterface(mqtt_host, mqtt_port, mqtt_user, mqtt_password)
class ConnectionInterfaceThread(Thread):
  def run(self):
    print 'Starting Connection'
    connection_interface.connect()

connection_thread = ConnectionInterfaceThread()
connection_thread.daemon = True
connection_thread.start()

print 'Starting...'

class Lectura(Thread):
  def run(self):
    print 'Starting GPS reading...	'
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
            print res
            connection_interface.send('location', res)

          print msg
        else:
          print "empty message"
      except:
        print 'ERROR'

x = Lectura()
x.modem = s
x.daemon = True
x.start()
print "COnfiguring GPS"
s.write('AT+CGPSURL="supl.google.com:7276"\r')
s.write('AT+CGPSSSL=0\r')
s.write('AT+CGPS=1,2\r')
while True:
  s.write('AT+CGPSINFO\r')
  time.sleep(5)
