import streams

import fatfs # import driver module
import os    # import file/directory management module

streams.serial()


# mount my SD card as volume 0 through SPI protocol
fatfs.mount('0:', {"drv": SPI0, "cs": D25, "clock": 1000000} )

# mount my SD card as volume 0 trough SD mode
# (be careful in choosing frequency (kHz) and bits supported by your board)
# fatfs.mount('0:', {"drv": SD1, "freq_khz": 20000, "bits": 1})

# create "zerynth.txt" file and open it for read/write operations
ww = os.open('0:zerynth.txt', 'w+')

# write a string on it, flushing data immediately (not waiting for file to be closed)
ww.write("Zerynth allows me to easily manage files, cool.", sync = True)


# ops, I forgot what I wrote...
# not a real problem problem using Zerynth

# back to the start
ww.seek(0)
print("I wrote: ", ww.read())

ww.close()

# files and directories in root folder?
print(os.listdir('.'))


# a folder for zerynth stuff is needed
if not os.exists("0:zerynth_stuff"):
    os.mkdir("0:zerynth_stuff")
    
# copy my cool file    
os.copyfile("zerynth.txt","zerynth_stuff/zerynth_cool.txt")
os.chdir("0:zerynth_stuff")

# check if anything went wrong
print("in ", os.getcwd())
print(os.listdir('.'))

print("SUCCESS!")
