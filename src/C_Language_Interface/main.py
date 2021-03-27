################################################################################
# C Interface
################################################################################

# Zerynth allows calling C code from Python


# Let's define a Python function decorated with c_native.
# This function has no body and will instead call
# the C function specified in the decorator.
# The source file(s) where to find the C function must be given (cdiv.c)
@c_native("_my_c_function",["cdiv.c"],[])
def c_division(a,b):
    pass


while True:
    # let's generate some random numbers
    a = random(0,100)
    b = random(0,10)
    try:
        # call the c_division function with the random values
        c = c_division(a,b)
        print(a,"/",b,"=",c)
    except Exception as e:
        print(e)
    sleep(1000)
