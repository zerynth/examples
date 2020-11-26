###############################################################################
# Zerynth oscilloscope
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
###############################################################################

import streams
import adc
   
streams.serial()

while True:
    value = adc.read(A4)
    conv = value*80//4095
    print("|","#"*conv," "*(80-conv),"|")
    sleep(200)
    