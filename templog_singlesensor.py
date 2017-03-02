#!/usr/bin/python

import time
import os
import glob
import RPi.GPIO as GPIO

######################
# Define Functions
######################

def led_on():
    GPIO.output(12,GPIO.LOW)
    return

def led_off():
    GPIO.output(12,GPIO.HIGH)
    return

def read_temp_raw():                         # Open file and read all lines
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    tries = 0
    lines = read_temp_raw()
    while ((lines[0].strip()[-3:] != 'YES') and (tries < 3)):    # If temp not ready wait and then re-read
        led_on()
        time.sleep(0.2)
        led_off()
        
        lines=read_temp_raw()
        tries = tries +1
        
    if (tries != 3):
        equals_pos=lines[1].find('t=')           # Once temp available, read from end of 2nd line
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)/1000.0   # Convert temp to degrees Celsius
        else:
            temp_c = 0.0
    else:
        temp_c = 99.99
    return temp_c

######################
# Start of Main Code
######################

# Configure GPIO for led drive
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

# Detect all temperature probes attached to 1-wire bus

print ("Detecting Temperature Sensors")

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
sensor_list = (glob.glob(base_dir + '28*'))
number_of_sensors  = len(sensor_list)

if number_of_sensors==0:
    print ("No sensors found")
else:
    print ("Found %s Sensors" %number_of_sensors)
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

print ("Done")
    
while (number_of_sensors!=0):

    led_on()
    
    # Read time
    localtime = time.asctime( time.localtime(time.time()) )
    ticktime  = int(time.time())
    with open('./temperature_log.csv', 'a') as f:
        f.write(localtime +", " +str(ticktime) +", " +str(read_temp()) +" C\n")    

    led_off()
    
    time.sleep(59)

