from carlog import logger
import RPi.GPIO as gpio
import time
try:
  gpio.setmode(gpio.BCM)
except:
  logger.info('error gpio setmode')
class ManejaAuto():
  def __init__(self):
    try:
      gpio.setmode(gpio.BCM)
      gpio.setup(17, gpio.OUT)
      gpio.setup(22, gpio.OUT)
      gpio.output(17, False)
      gpio.output(22, False)
    except:
      logger.info('error gpio')

  def activar_motor(self, comando):
    logger.info('executting command: ')
    try:
      if comando == '1':
        gpio.output(17, True)
        gpio.output(22, False)
      elif comando == '2':
        gpio.output(17, False)
        gpio.output(22, True)
    except:
      logger.info('error gpio output')

