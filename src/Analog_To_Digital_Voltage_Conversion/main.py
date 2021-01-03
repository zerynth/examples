################################################################################
# Analog Read to Voltage
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams
import adc      # import the adc module  

#create a serial port stream with default parameters
streams.serial()

while True:
       
    #read the input on analog pin 0
    sensor_value = adc.read(A0)
    
    #convert the analog reading (which goes from 0 - 4095.0) to a voltage (0 - 3.3V):
    voltage = sensor_value * (3.3 / 4095.0)
    
    #print out the raw and converted values:
    print("sensor raw value:", sensor_value,"Voltage:",voltage)
    
    sleep(300)


