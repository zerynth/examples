###############################################################################
# ZFileSystem SD card
################################################################################

import fs

while True:
    fs.mount("/mnt", 0)

    #read and write an existing file
    f = fs.FileIO("mnt/test.txt", "r")
    print(f.read())
    f.close()

    f = fs.FileIO("/mnt/test.txt","w")
    f.write("first row: test 01")
    f.write("second row: test 02")
    print(f.readline())
    print(f.readline())
    f.close()
    
    # create a new file and read it back
    f = fs.FileIO("/mnt/test02.txt","w")
    f.write("Hello Zerynth!")
    f.close()

    f = fs.FileIO("/mnt/test02.txt","r")
    print(f.read())
    f.close()

    fs.unmount("/mnt")

    sleep(1000)