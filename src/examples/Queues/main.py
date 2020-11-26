################################################################################
# Queues
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

import threading
import streams
import queue


streams.serial()

# create a bounded queue
q = queue.Queue(maxsize=20)

# keep producing an element every 100 millis
def producer(id):
    while True:
        try:
            x = random(0,100)
            print("producer",id,"->",x)
            q.put(x)
        except Exception as e:
            print(e)
        sleep(100)

# keep consuming an element every 1 second
def consumer(id):
    while True:
        try:
            print("consumer",id,"<-",q.get())
        except Exception as e:
            print(e)
        sleep(1000)

# start everyone
thread(producer,0)
thread(consumer,1)
thread(consumer,2)

while True:
    isfull = q.full()
    print("Queue is full?",isfull)
    if isfull:
        # clear queue if full
        print("Clearing queue")
        q.clear()
    sleep(5000)
