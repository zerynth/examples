################################################################################
# LED Fade
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi,  D. Mazzei
###############################################################################

import pwm

duty=0

pinMode(LED0,OUTPUT) # set the LED pin as output:

while True:
    for i in range(-100,100,1):   # create a loop for ranging the duty cycle from 0 to 100 MICROS
        duty=100-abs(i)
        pwm.write(LED0.PWM,100,duty,MICROS)     # set the pwm at the calculated duty with a fixed period of 100 MICROS
        sleep(10) # update the PWM every 10 millis  
