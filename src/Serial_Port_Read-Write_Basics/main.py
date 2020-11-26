################################################################################
# Serial Port Basics
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams
# creates a serial port and name it "s"
s=streams.serial()

while True:
    print("Write some chars on the serial port and terminate with \\n (new line)")
    line=s.readline() # read and return any single character available on the serial port until a \n is found
    print("You wrote:", line)
    print()
    sleep (300)
      
    
   