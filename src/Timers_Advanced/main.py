################################################################################
# Timers Advanced Use

# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import timers
import streams

# create a serial port with default parameters
streams.serial()

# create new timers
tsec=timers.timer()
tminute=timers.timer()     
tshoot=timers.timer()

seconds=0
minutes=0

# define a function to call when the timer for seconds elapses
def secondpassed():
    global seconds
    seconds +=1
    print(seconds,"  seconds")
    if seconds==60:
        seconds=0

# define a function to call when the timer for minutes elapses
def minutepassed():
    global minutes
    minutes +=1
    print(minutes,"  minutes")
    
# define a function to call when the one shot timer elapses
def shootpassed():
    print("1 second ago was 1:30")
    
# start the timers for minutes and seconds
tsec.interval(1000,secondpassed)
tminute.interval(60000,minutepassed)
tsec.start()
tminute.start()
    
while True:
    
    if seconds==30 and minutes==1:                               # do a check on passed time to trigger a oneshot timer 
        tshoot.one_shot(1000, shootpassed)                       # this is a oneshot timer, it executes only one time
                
    print("timer minutes runs since:", tminute.get(),"timer seconds runs since:",tsec.get(), "millisec")         #just print the current value since start or last reset
    sleep(2500)                 #run every 2500 millisec