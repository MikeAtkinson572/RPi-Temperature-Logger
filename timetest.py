#!/usr/bin/python

import time
import os
import glob

######################
# Define Functions
######################



######################
# Start of Main Code
######################

# Detect all temperature probes attached to 1-wire bus


while True:
    # Read time
    localtime = time.asctime( time.localtime(time.time()) )
    ticktime  = time.time()
    
    # Read all temp sensors
    # Write entry to log file
    with open('./temperature_log.csv', 'a') as f:
        f.write(localtime +',' +'\n')

    # Wait for 5 seconds
    time.sleep(5)
    


    
