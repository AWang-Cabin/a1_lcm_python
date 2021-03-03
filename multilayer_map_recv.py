#lcm
import lcm
from exlcm import multilayer_map_t

import numpy as np

layers = 4
x_size = 20
y_size = 20
multimap = np.zeros((4,20,20))

# map callback function
def multimap_handler(channel, data):
    msg = multilayer_map_t.decode(data)
    global multimap
    multimap = np.array(msg.multimap)
    print("Received message on channel \"%s\"" % channel)


#decode map data
lc1=lcm.LCM()
subscription1 = lc1.subscribe("multimap", multimap_handler)
# n=0
# max=0
try:
    while True:
        lc1.handle()# call data
        # n=n+1
        # print(n)
        # for k in range(layers):
        #     print(k, end="\n")
        #     for i in range(x_size):
        #         for j in range(y_size):
        #             if multimap[1][i][j]-multimap[2][i][j]>max:
        #                 max=multimap[1][i][j]-multimap[2][i][j]
        #             print(multimap[k][i][j],end=" ")
        #         print(end="\n")
        # print("height-range:",max,end="\n")
except KeyboardInterrupt:
    pass

