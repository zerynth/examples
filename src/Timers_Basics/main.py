################################################################################
# Timers Basics
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import timers
import streams

# create a serial port with default parameters
streams.serial()

# create a new timer
t=timers.timer()
# start the timer
t.start()

minutes=0
   
while True:
    
    if t.get()>= 60000:        #check if 60 seconds are passed
        t.reset()              #timer can be reset
        minutes +=1
    seconds=t.get()//1000
    print("time is:", minutes,":",seconds) #just print the current value since timer start or last reset
    print("System time is:", timers.now(), "(millis)") #timers.now() gives the system time in milliseconds since program start
    print()
    
    sleep(500)                 #run every 500 millisec