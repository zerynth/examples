################################################################################
# Interrupt Debounce
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# import streams
import streams
# import pwm for testing
import pwm


# CONNECT pin D3 to PIN D2 for this example to work!

streams.serial()

def on_touch_up():
    print("touched UP")

def on_touch_dn():
    print("touched DN")
    

    
try:    
    # D2 will call touch_up on rise and touch_dn on fall with different debounce times
    onPinRise(D2,on_touch_up,debounce=500)
    onPinFall(D2,on_touch_dn,debounce=300)
except Exception as e:
    print(e)




while True:
    for x in [100,200,300,400,500,600,700,800,900]:
        print("--->",x, 1000-x)
        # start pwm on D3 with the current period
        pwm.write(D3.PWM,1000,x)
        # now wait and check if debounce is working
        sleep(5000)