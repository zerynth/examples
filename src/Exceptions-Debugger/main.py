################################################################################
# Exception-Debugger Basics
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi,  D. Mazzei
###############################################################################

import streams

streams.serial()

while True:
    for x in range(-10,10,1):   # create a loop ranging on the integers between -10 and 10
        
        try:                    # open the Exception monitoring scope
            value=100//x        # when x=0 this will results in a DivisionByZero!
            print(value)
        except Exception as e:  # capture any raised exception as e
            print(e)            # print the content of e to monitor where the program is faulting
                                # click on the console X icon to open the Zerynth debugger window 
        sleep(1000)    
      
