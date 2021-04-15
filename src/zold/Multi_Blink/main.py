################################################################################
# Multi-Blink
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# Initialize the digital pins where the LEDs are connected as output
pinMode(D2,OUTPUT)
pinMode(D8,OUTPUT)
pinMode(D5,OUTPUT)

# Define the 'blink' function to be used by the threads
def blink(pin,timeON=100,timeOFF=100): # delayON and delayOFF are optional parameters, used as default 
                                         # if not specified when you call the function
    while True:
        digitalWrite(pin,HIGH)   # turn the LED ON by making the voltage HIGH
        sleep(timeON)            # wait for timeON 
        digitalWrite(pin,LOW)    # turn the LED OFF by making the voltage LOW
        sleep(timeOFF)           # wait for timeOFF 

# Create three threads that execute instances of the 'blink' function.     
thread(blink,D2)             # D2 is ON for 100 ms and OFF for 100 ms, the default values of delayON an delayOFF
thread(blink,D8,200)         # D8 is ON for 200 ms and OFF for 100 ms, the default value of delayOFF
thread(blink,D5,500,200)     # D5 is ON for 500 ms and OFF for 200 ms