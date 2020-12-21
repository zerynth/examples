################################################################################
# Input Capture Unit as PWM Analyzer
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import pwm 
import icu
import streams

# create the serial port using default parameters  
streams.serial()

# define a pin where a button is connected, you can use the Nucleo button pin as input or change it with any other digital pin available

# this is the pin the button is connected to; for the various supported boards, Zerynth automatically translates it 
# to the board button. On Arduino DUE the user button isn't installed, so this line rises a compilation error.
# On Arduino DUE, change it to the pin your button is connected to or comment this line (see below)
buttonPin=BTN0


# define the ICU pin. D5 works with Arduino footprint boards while with Particle boards D0 can be used 
captPin=D5.ICU  # On Arduino like boards
#captPin=D0.ICU  # On Particle boards

# define the PWM pin. D13 works with Arduino footprint boards (and is also connected to a LED) while with Particle boards A4 can be used
pwmPin=D13.PWM # On Arduino like boards 
#pwmPin=A4.PWM # On Particle boards

# set the pin as input with PullUp, the button will be connected to ground
pinMode(buttonPin, INPUT_PULLUP)

# define a function for printing capture results on the serial port
def print_results(y):
    print("Time ON is:", y[0],"micros")
    print("Time OFF is:",y[1],"micros")
    print("Period is:", y[0]+y[1], "micros")
    print()
    
# define a global variable for PWM duty cycle and turn on the PWM

duty=10
pwm.write(pwmPin,100, duty,MICROS) #pwm.write needs (pn, period, duty, time_unit)

# define the function to be called for changing the PWM duty when the button is pressed
def pwm_control():
    global duty
    duty= duty+10
    if duty>=100:
        duty=0
    pwm.write(pwmPin, 100, duty,MICROS)
    print("Duty:", duty, "millis")
    
# Attach an interrupt on the button pin waiting for signal going from high to low when the button is pressed.
# pwm_control will be called when the interrupt is fired.
# If you are on Arduino DUE and you haven't connected any button comment the following line 
# you will not change the PWM duty but you can still test the ICU capture
onPinFall(buttonPin, pwm_control)

while True:
    # start an icu capture to be triggered when the pin rise.
    # this routine acquires 10 steps (HIGH or LOW states) or terminates after 50000 micros
    # this is a blocking function
    x = icu.capture(captPin,LOW_TO_HIGH,10,50000,MICROS)
    print("captured")
    # x is a list of step durations in microseconds, pass it to the printing function and check the serial console
    print_results(x)
    
    sleep(1000)
    
