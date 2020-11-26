###############################################################################
# Led Blink
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
###############################################################################

# D0 to D127 represent the names of digital pins
# On most Arduino-like boards Pin D13 has an on-board LED connected.
# However Zerynth abstracts the board layout allowing to use LED0, LED1, etc as led names.
# In this example LED0 is used.

pinMode(LED0,OUTPUT)

# loop forever
while True:
    digitalWrite(LED0, HIGH)  # turn the LED ON by setting the voltage HIGH
    sleep(1000)               # wait for a second
    digitalWrite(LED0, LOW)   # turn the LED OFF by setting the voltage LOW
    sleep(1000)               # wait for a second

