#!/usr/bin/python

import time
import os
import glob
import RPi.GPIO as GPIO


######################
# Start of Main Code
######################

# Configure GPIO for led drive
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

   
while True:
    # Turn LED on
    GPIO.output(12,GPIO.LOW)
    time.sleep(1)
    
    # Turn LED off
    GPIO.output(12,GPIO.HIGH)
    time.sleep(1)

