###############################################################################
# Hello TFLite
###############################################################################


# Import the tensorflow lite module
from tflite import tflite
import gc

# create a model from ml/model.c
# in this example the model approximates y = sin(x)
model = tflite.Model()


c=0.0
while True:
    # print something
    #print("Hello Zerynth!",gc.info())
    # set input at index 0
    model.set(0,c)
    # invoke the model
    model.invoke()
    # retrieve output at index 0
    x = model.get(0)
    # print the value!
    val = int(80*x)
    if val>0:
        print(80*" ",val*"#")
    else:
        val = -val
        print((80-val)*" ",val*"#")

    c+=0.1
    sleep(100)
