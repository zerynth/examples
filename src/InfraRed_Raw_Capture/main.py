################################################################################
# ICU Capture IR Packets
#
# Created by Zerynth Team 2015 CC
# Authors: L. Rizzello, G. Baldi, D. Mazzei  
################################################################################

import icu
import streams
import pwm

streams.serial()

# Set the pin the IR receiver is connected to.
# In this example D2 is used: if you happen to have a TOI Shield on an Arduino compatible board
# you are good to go.
ir_pin = D2.ICU # when you want to use a particular pin function, just use the dot notation


def IR_capture():
    while True:
        print("Capturing...")
        # Starts capturing from the icu configured pin.
        # The capture starts from a selected trigger (in this case capture will start when the pin first goes from
        # HIGH to LOW).
        # The max number of samples to be collected and a maximum time window are specified.
        
        # Play with max number and time window to fit your remote protocol.
        # The following values are for the NEC IR (used by LG) protocol
        x = icu.capture(ir_pin,LOW,67,68,pull=HIGH)
        print(x,"\n captured n samples:",len(x))
               
    
# captures in a different thread
thread(IR_capture)

while True:
    print("alive!")
    sleep(1000)