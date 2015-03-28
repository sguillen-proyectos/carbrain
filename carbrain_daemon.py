#!/usr/bin/python

import time
import thread
import utils as _
from carlog import logger
from gpstrack import start_tracker

# thread.interrupt_main() -> to kill process from thread

if not _.check_internet():
  logger.info('No internet connection')
  exit(1)
else:
  logger.info('Starting main program')
  start_tracker()

  while True:
    if not _.check_internet():
      exit(1)
    time.sleep(30) # Check internet every 30 secons
