################################################################################
# Interrupt Basics
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams

# create a serial port stream with default parameters
streams.serial()

# define where the button and the LED are connected
# in this case BTN0 will be automatically configured according to the selected board button
# change this definition to connect external buttons on any other digital pin
buttonPin=BTN0 
ledPin=LED0  # LED0 will be configured to the selected board led

# configure the pin behaviour to drive the LED and to read from the button  
pinMode(buttonPin,INPUT_PULLUP)
pinMode(ledPin,OUTPUT)

# define the function to be called when the button is pressed
def pressed():
        print("touched!")
        digitalWrite(ledPin,HIGH) # just blink the LED for 100 millisec when the button is pressed
        sleep(100)
        digitalWrite(ledPin,LOW)

# attach an interrupt on the button pin and call the pressed function when it falls
# being BTN0 configured as pullup, when the button is pressed the signal goes to from HIGH to LOW.
# opposite behaviour can be obtained with the equivalent "rise" interrupt function: onPinRise(pin,fun)
# hint: onPinFall and onPinRise can be used together on the same pin, even with different functions
onPinFall(buttonPin,pressed)



