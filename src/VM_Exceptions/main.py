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

#test 1: reset on uncaught exception and print trace (Default)
vm.set_option(vm.VM_OPT_RESET_ON_EXCEPTION,1)
vm.set_option(vm.VM_OPT_TRACE_ON_EXCEPTION,1)

#test 2: don't reset on uncaught exception but print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_EXCEPTION,0)
# vm.set_option(vm.VM_OPT_TRACE_ON_EXCEPTION,1)

#test 3: don't reset on uncaught exception and don't print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_EXCEPTION,0)
# vm.set_option(vm.VM_OPT_TRACE_ON_EXCEPTION,0)

#test 3: reset on uncaught exception but don't print trace (Default)
# vm.set_option(vm.VM_OPT_RESET_ON_EXCEPTION,1)
# vm.set_option(vm.VM_OPT_TRACE_ON_EXCEPTION,0)


def thread_fn_exc():
    for i in range(5):
        print("TH working",i)
        sleep(1000)
    x=1/0

# launch thread
thread(thread_fn_exc)

while True:
    sleep(2000)
    #let's print some VM info
    nfo = vm.info()
    print("--------------")
    print("VM uid ",nfo[0])
    print("Target ",nfo[1])
    print("Version",nfo[2])
    print("--------------")

