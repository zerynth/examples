###############################################################################
# ZFileSystem internal
################################################################################

import fs

while True:

    #read an existing file
    f = fs.open("/zerynth/test.txt", "r")
    print(f.read())
    f.close()

    # create a new file and read it back
    f = fs.open("/zerynth/test02.txt","w")
    f.write("first row: test 01\n")
    f.write("second row: test 02\n")
    f.close()
    f = fs.open("/zerynth/test02.txt", "r")
    print(f.read())
    f.close()

    sleep(1000)