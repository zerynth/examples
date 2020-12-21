################################################################################
# Serial Advanced
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams

s = streams.serial()

# Testing various serial port reading methods
   
while True:
    print("write some chars and send it to the board")
    char=s.read() # read and return any single character available on the serial port one by one
    print("This is the first char you wrote:",char)
    print() # add a line space for improving the serial console ouput readability
    
    sleep(500) # waiting for the serial buffer to fill
    length=s.available() # check if data are available on the port and count them
    chars=s.read(length) # read all the bytes available in the buffer an return the bytearray 
    print("This are the other", length, "chars you wrote:",chars)
    print() # add a line space for improving the serial console view
    
    print("write a line ending it with return or enter")
    line=s.readline() # read until a line terminator \n is found, then return a bytearray
    print("This is the line you wrote:",line)