################################################################################
# Analog Read
# 
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams  # import the streams module
import adc      # import the adc driver 

# create a stream linked to the default serial port
streams.serial() 

while True:
    
# Basic usage of ADC for acquiring the analog signal from a pin   
    value = adc.read(A0)
    print("One sample:",value)

# The complete definition of adc.read() is adc.read(pin, samples=1) 
# For an advanced usage of adc.read refer to the official Zerynth documentation

#acquire 10 samples with default sampling period    
    value2 = adc.read(A0,10)
    print("10 samples:\n",value2)
    
#acquire 3 samples from the first 4 analog pins of the board with default sampling period    
    value3= adc.read([A0,A1,A2,A3],3)
    print("3 samples from A0, A1, A2 and A3:\n",value3)

    print()
    sleep(300)