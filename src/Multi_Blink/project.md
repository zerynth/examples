Multi LEDs Blink with threads
===================================
This examples shows how to use ZERYNTH threads for driving three LEDs with asymmetric and different blinking rates. 

Each Thread in ZERYNTH is a sort of separated and parallel process that runs autonomously on your board. 
With threads you can design your algorithm architecture assuming parallelism that is typical of high level programming languages. 
In this code a function is defined and then instanced by three threads creating a pool of parallel processes where three LEDs are driven 
at different frequencies. 

Moreover, thanks to Python argument passing, default values can be defined for function inputs. 
This way you can launch threads without specifying all the inputs required by the function, default values will fill the holes.
In this case all the parameters following 'blink' are passed to the functions as arguments.
thread(blink,pin,delayON,delayOFF) is equivalent to thread(blink(pin,delayON,delayOFF)).

tags: [Multi-Thread, First Steps, Digital I/O]
groups:[First Steps]  