#!/usr/bin/python

import time
import os
import sys
import glob
import RPi.GPIO as GPIO
import urllib.parse            # URL functions
import urllib.request          # URL functions
import urllib.error            # URL functions
import http.client


######################
# THINGSPEAK VERSION
######################


######################
# Define 'Constants'
######################
INTERVAL      = 60    # Seconds
THINGSPEAKKEY = '8FXR7VVHNXB9Q3C2'
THINGSPEAKURL = 'http://api.thingspeak.com/update'


######################
# Define Functions
######################

def led_on():
    GPIO.output(11,GPIO.LOW)
    return

def led_off():
    GPIO.output(11,GPIO.HIGH)
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


def sendData(url,key,field1,temp1,field2,temp2):
  
  # Send event to internet site

  params = urllib.parse.urlencode({'key':key, 'field1':temp1, 'field2':temp2})
  headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  conn = http.client.HTTPConnection("api.thingspeak.com:80")

  try:
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    conn.close()
  except:
    print("Connection failed")
  

######################
# Start of Main Code
######################

# Configure GPIO for led drive
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# Flash LED to indicate booted

flashes = 0
while (flashes<5):
    led_on()
    time.sleep(0.1)
    led_off()
    time.sleep(0.1)
    flashes += 1

########################################
# INITIALISATION AND DIAGNOSTICS
########################################

# Write header to log file
with open('./temperature_log.csv', 'a') as f:
    f.write("\n\n#################################\n")
    f.write("# RESTARTING TEMPERATURE LOGGER #\n")
    f.write("#################################\n\n")
        
# Detect all temperature probes attached to 1-wire bus

print ("\n\n##### Detecting Temperature Sensors")

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
sensor_list = (glob.glob(base_dir + '28*'))
number_of_sensors  = len(sensor_list)

starttime = int(time.time())
localtime = time.asctime( time.localtime(time.time()) )

# Initial Status report
print("##### Logging Start: " + localtime)
print("##### Number of Sensors: " +str(number_of_sensors))

with open('./temperature_log.csv', 'a') as f:
    f.write("##### Logging Start: " + localtime +"\n")
    f.write("##### Number of Sensors: " +str(number_of_sensors) +"\n")
    f.write("##### Output format: elapsed time (s), ")
    for sensor in sensor_list:
        f.write("#" +sensor[-15:] +", ")
    f.write("\n")



######################################################
# MAIN LOOP
######################################################

while (number_of_sensors!=0):
    # Read time
    ticktime  = int(time.time())
    elapsedtime = (ticktime - starttime)
    localtime = time.asctime( time.localtime(time.time()) )  
    
    led_on()
    with open('./temperature_log.csv', 'a') as f:
        f.write(localtime +", " +str(elapsedtime))
        for device_folder in sensor_list:
            device_file = device_folder + '/w1_slave'
            temp1 = read_temp()
            f.write(", " +str(temp1))
        f.write("\n")
    led_off()

    sendData(THINGSPEAKURL,THINGSPEAKKEY,'field1',temp1,'field2',temp1)
    sys.stdout.flush()
    
    # It takes approx 1 second to read and process each sensor, so...
    time.sleep((INTERVAL - number_of_sensors))

