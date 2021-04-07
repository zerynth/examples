###############################################################################
# ZFileSystem SD card
################################################################################

import fs

while True:
    fs.mount("/sd", fs.SD, 10000000)

    #read an existing file
    f = fs.open("/sd/test.txt", "r")
    print(f.read())
    f.close()
    
    # create a new file and read it back
    f = fs.open("/sd/test02.txt","w")
    f.write("first row: test 01\n")
    f.write("second row: test 02\n")
    f.close()

    f = fs.FileIO("/sd/test02.txt","r")
    print(f.read())
    f.close()

    fs.unmount("/sd")

    sleep(1000)