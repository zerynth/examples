################################################################################
# strformat
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import streams

streams.serial()

print("Starting!")
sleep(1000)

# a data tuple
tt = ("string",-21,15.23,32)
# a data dictionary
dd = {
      "thing":"string",
      "number":1,
      "float":1.0,
      "hex":32  
}

# let's format :)
while True:
    try:
        # basic formatting
        print("%% this is a %s, this is a %d, this is a %f, this is a %x, this is a %%"%tt)
        # named keys formatting
        print("%% this is a %(thing)s, this is a %(number)d, this is a %(float)f, this is a %(hex)x, this is a %%"%dd)
        # width & precision
        print("%s %8d %f %d"%tt)
        print("%s %08.7d %f %d"%tt)
        # width & precision & left alignment & sign
        print("%s %-010.9d %f %d"%tt)
        print("%s %-010.9d %2.0f %d"%tt)
        print("%s %-010.9d %2.5f %d"%tt)
        print("%s %-010.9d %12.5f %d"%tt)
        print("%s %-010.9d %-12.5f %d"%tt)
        print("%s %-010.9d %012.15f %d"%tt)
        print("%s %+010.9d %012.15f %d"%tt)
        print("%s % 010.9d %012.15f %d"%tt)
        # width & precision for strings
        print("%15.3s % 010.9d %012.15f %d"%tt)
        # variable width & precision
        print("%x %3.*d"%(123456,5,6))
    except Exception as e:
        print(e)
    sleep(5000)
