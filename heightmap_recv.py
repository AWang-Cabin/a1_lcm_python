
#lcm
import lcm
from exlcm import heightmap_t
#common
import math
import numpy as np

size = 100
height=[[[]for i in range(size)]for i in range(size)]

# heightmap callback function
def heightmap_handler(channel, data):
    msg = heightmap_t.decode(data)
    heightmap=np.array(msg.heightmap)
    # print(heightmap)
    # print("Received message on channel \"%s\"" % channel)
    for i in range(size):
        for j in range(size):
            global height
            height[i][j].append(heightmap[i][j])
            print(i ,j,end=" ")
            print(" heightmap = %s" % str(heightmap[i][j]))

#decode heightmap data
lc1=lcm.LCM()
subscription1 = lc1.subscribe("heightmap", heightmap_handler)
try:
    while True:
        lc1.handle()# call heightmap data
except KeyboardInterrupt:
    pass

