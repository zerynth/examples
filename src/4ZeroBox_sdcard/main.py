###############################################################################
# 4ZeroBox SD card
################################################################################

from bsp import board
import fs

board.init()
sleep(5000)

while True:
    fs.mount("/sd", fs.SD, 10000000)

    # read an existing file
    f = fs.open("/sd/test.txt","r")
    print(f.read())
    f.close()

    # create a file and read it back
    f = fs.open("/sd/test2.txt","r")
    print(f.tell())
    print(f.size())
    print(f.read(1))
    print(f.tell())
    print(f.read())
    print(f.tell())
    f.seek(0, fs.SEEK_SET)
    print(f.read())
    f.close()

    fs.unmount("/sd")
    sleep(1000)