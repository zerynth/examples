################################################################################
# Dac Basic
#
# Created by Zerynth Team 2015 CC
# Authors: L. Rizzello
################################################################################

import streams
import adc # for analogRead

import dac


def readInput():
    while True:
        print("reading A1: ",analogRead(A1))
        sleep(500)

streams.serial()
pinMode(A1,INPUT)

# read input in a separate thread
thread(readInput)

my_dac = dac.DAC(D8.DAC)
my_dac.start()

# circular mode: continuously repeat the input buffer
my_dac.write([100,200,900,800],1000,MILLIS,circular=True)
