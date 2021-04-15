################################################################################
# Sensor Driven Multi-Blink
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# This example requires an analog sensor and three LEDs
import streams
import adc

# create a serial port stream with default parameters
streams.serial()

# set the A1 pin as analog input and D8, D9, D10 as outputs to drive the LEDs. 
pinMode(A1,INPUT_ANALOG)
pinMode(D10,OUTPUT)
pinMode(D9,OUTPUT)
pinMode(D8,OUTPUT)

# creates two arrays for storing global variables to be used in the blinking threads
freq=[1,1,1]        
pin=[D8,D9,D10]    

# define the generic blinking function to be used for driving the LEDs
# this function takes as input the index identifying the LED, then uses the global freq and pin arrays to dynamically drive the LEDs
def blink(Npin):
    while True:
        digitalWrite(pin[Npin],HIGH)
        sleep(freq[Npin])
        digitalWrite(pin[Npin],LOW)
        sleep(freq[Npin])

# define an analog sensor sampling function that acquires the raw data and converts it to the three LED frequencies
def sampling():
    global freq
    while True:
        value = adc.read(A1)
        freq[0] = value//10
        freq[1] = freq[0] * 2
        freq[2] = freq[0] * 4
        sleep(50)

# launch the four threads        
thread(sampling)
thread(blink,0)
thread(blink,1)
thread(blink,2)

# The main loop is used only for printing out at reasonable speed the calculated frequencies in term of waiting times 
while True:
    print("Wait times are", freq)
    sleep(500)
