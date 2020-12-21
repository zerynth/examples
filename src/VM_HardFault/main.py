################################################################################
# Zerynth VM Options
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################
import streams
import vm

streams.serial()

#let's set some VM options: uncomment the test you want to try, comment the others

#test 1: reset on hard fault and print trace (Default)
vm.set_option(vm.VM_OPT_RESET_ON_HARDFAULT,1)
vm.set_option(vm.VM_OPT_TRACE_ON_HARDFAULT,1)

#test 2: don't reset on hard fault but print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_HARDFAULT,0)
# vm.set_option(vm.VM_OPT_TRACE_ON_HARDFAULT,1)

#test 3: don't reset on hard fault and don't print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_HARDFAULT,0)
# vm.set_option(vm.VM_OPT_TRACE_ON_HARDFAULT,0)

#test 3: reset on hard faultbut don't print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_HARDFAULT,1)
# vm.set_option(vm.VM_OPT_TRACE_ON_HARDFAULT,0)


# here is a function that causes a hard fault by writing to NULL (in c)
@c_native("_hf_function",["hf.c"],[])
def armageddon():
    pass


while True:
    print("Releasing the Armageddon in 2 sec...:-@")
    sleep(2000)
    armageddon()
