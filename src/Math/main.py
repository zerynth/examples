###############################################################################
# Math module
#
# Created by Zerynth Team 2017 CC
# Authors: G. Baldi
###############################################################################
import streams
import math 

streams.serial()


while True:
    # loop over angles in degrees
    print("---> TRIGONOMETRY!")
    for angle in range(0,360*3,10):
        # convert to radians
        r = math.radians(angle)
        # take the sin
        s = math.sin(r)
        # calculate offset...
        sl = int(40*s)
        # ...and print!
        if sl>=0:
            print(" "*40,"#"*sl)
        else:
            print(" "*(40+sl),"#"*(-sl))
        sleep(50)
    sleep(1000)

    # loop from -5 to 0 in 0.05 increments
    print("---> EXPONENTIALS")
    x = -5
    incr = 0.05
    while x<0:
        # take the exp...
        y = math.exp(x)
        # ...and print!
        print("#"*int(y*80))
        # do not forget to increment x
        x = x + incr
        sleep(50)
    sleep(1000)
    
    print("---> ROOTS and POWERS")
    # loop from 1 to 100
    print(" a   |  b   |  c   | math.sqrt(a*a*+b*b)")
    print("----------------------------------------")
    for i in range(0,100):
        # let's generate and test Pythagorean Triples!
        # select n and m
        m = 1
        n = 0
        while m>=n:
            n = random(1,30)
            m = random(1,30)
        
        a = math.pow(n,2)-math.pow(m,2)
        b = 2*m*n 
        c = math.pow(n,2)+math.pow(m,2)
        a2 = math.pow(a,2)
        b2 = math.pow(b,2)
        p = math.sqrt(a2+b2)
        
        print("%4.0f | %4.0f | %4.0f | %4.0f"%(a,b,c,p))
        sleep(100)
    sleep(1000)
