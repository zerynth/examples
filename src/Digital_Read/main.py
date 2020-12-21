################################################################################
# Digital Read Basics
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams

# create a serial port stream with default parameters  
streams.serial()

# configure pin D5 in input mode
pinMode(D5, INPUT_PULLUP)

# loop forever, printing the value of D5
while True:
    print(digitalRead(D5))
    sleep(500)  