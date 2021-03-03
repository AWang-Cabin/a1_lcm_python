#lcm
import lcm
from exlcm import aroundfeet_map_t
import select
import numpy as np

aroundmap = np.zeros(36)

# map callback function
def aroundmap_handler(channel, data):
    msg = aroundfeet_map_t.decode(data)
    global aroundmap
    aroundmap = np.array(msg.aroundfeet_map)
    print("\nReceived message on channel \"%s\"" % channel)


#decode map data
lc1=lcm.LCM()
subscription1 = lc1.subscribe("aroundmap", aroundmap_handler)

try:
    timeout = 0.1  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc1.fileno()], [], [], timeout)
        if rfds:
            lc1.handle()
        else:
            print("Do something else...")
        # for i in range(4):
        #     print(i,end=" ")
        #     for j in range(9):
        #         print(aroundmap[i*9 + j], end=" ")
        #     print(end="\n")
        # print(aroundmap)

except KeyboardInterrupt:
    pass

