# -*- coding: utf-8 -*-
import logging
import time

def handler(event, context):
  logger = logging.getLogger()
  logger.info('hello world')
  time.sleep(20)
  return '{"outputKey": "outputValue"}'