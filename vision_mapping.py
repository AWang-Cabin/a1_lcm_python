#Created on 2020.11.1

# Subscribe heightmap(2m*2m) and corresponding traversability score from ROS by LCM,
# and draw heightmap-units(0.04m*0.04m) with their traversability, if the color of heightmap box is green,
# the terrain is relatively safe for robot, but if the color is red, the terrain is challenging for robot.

#  ________        _________                            ___________
# |        |      |         | --->   HEIGHT_MAP    --> |           |
# | CAMERA |  --> | ROS-LCM |                          |  PYBULLET |
# |________|      |_________| --->TRAVERSABLITY_MAP--> |___________|

# To run this file, you need INSTALL:
#       Python3.5 & Pybullet
#       LCM (Lightweight Communications and Marshalling)
#       ROS KINETIC(for Ubuntu16.04) / ROS MELODIC(for Ubuntu18.04)
#       PCL (Point Cloud Library)
#       your depth camera driven package and corresponding ROS package

# Run step:
# 1. new terminal: $ sh roslaunch_vision.sh      (do not use sudo)
# 2. run this file

#pybullet
import pybullet as p
import pybullet_data
#lcm
import lcm
from exlcm import traversability_float_t
from exlcm import heightnew_t
#common
import math
import numpy as np

# ignore the size difference of height and trav_score
height=[[[]for i in range(101)]for i in range(101)]
trav_score=[[[]for i in range(100)]for i in range(100)]
hm=heightnew_t()
trav=traversability_float_t()
# heightmap callback function
def heightmap_handler(channel, data):
    msg = heightnew_t.decode(data)
    heightmap=np.array(msg.map)
    # print(heightmap)
    # print("Received message on channel \"%s\"" % channel)
    for i in range(101):
        for j in range(101):
            global height
            height[i][j].append(heightmap[i][j])
            print(i ,j,end=" ")
            print(" heightmap = %s" % str(heightmap[i][j]))

# traversabilitymap callback function
def travmap_handler(channel, data):
    msg = traversability_float_t.decode(data)
    travmap=np.array(msg.map)
    # print(heightmap)
    # print("Received message on channel \"%s\"" % channel)
    for i in range(100):
        for j in range(100):
            global trav_score
            trav_score[i][j].append(travmap[i][j])
            # print(i ,j,end=" ")
            # print(" scoremap = %s" % str(travmap[i][j]))

lc1=lcm.LCM()
lc2=lcm.LCM()
subscription1 = lc1.subscribe("heightmapnew", heightmap_handler)
subscription2 = lc2.subscribe("traversability_float", travmap_handler)
lc1.handle()# call heightmap data
lc2.handle()# call travmap data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setTimeStep(1. / 5000.)
p.loadURDF("plane100.urdf", useMaximalCoordinates=True) # bodyid=0
p.getCameraImage(480,320)

h=np.array(height)
score=np.array(trav_score)
rangex = 100
rangey = 100

for i in range(0,rangex,2):
    for j in range(0,rangey,2):
        # 'cause the most box bodies pybullet can build is around 1000, we cannot use initial resolution(0.02*0.02m),
        # To draw the map, we must reduce resolution to 0.04*0.04m and recompute their heights and scores.

        # avg_height=(h[i][j]+h[i][j+1]+h[i+1][j]+h[i+1][j+1])/4
        avg_height=h[i][j]
        avg_score=score[i][j]#+score[i][j+1]+score[i+1][j]+score[i+1][j+1])/4
        tmp=avg_height*100
        if tmp%2<1:
            avg_height=(math.floor(tmp))/100
        else:
            avg_height=(math.ceil(tmp))/100

        # visualize the score map by different colors
        if avg_height>0.02:
            if avg_score>1.0:
                box_rgb=[1.0,1.0,0.0,1.0]#yellow
            elif avg_score<=1.0:
                box_rgb=[0.5,1.0,0.0,1.0]#blue

            # the visual shape and collision shape can be re-used by all createMultiBody instances (instancing)
            meshScale = [0.04,0.04,avg_height] # box size[len,width,height]
            shift = [0, 0, 0]
            # box's color property
            visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH,
                                    fileName="data/marble_cube.obj",
                                    rgbaColor=box_rgb,
                                    specularColor=[0, 0, 0],
                                    visualFramePosition=shift,
                                    meshScale=meshScale)
            # box's collision property
            collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                          fileName="data/marble_cube.obj",
                                          collisionFramePosition=shift,
                                          meshScale=meshScale)
            # add boxes
            p.createMultiBody(baseMass=0,
                          baseInertialFramePosition=[0, 0, 0],
                          baseCollisionShapeIndex=collisionShapeId,
                          baseVisualShapeIndex=visualShapeId,
                          basePosition=[((-rangex / 2) + i) * meshScale[0] * 1,
                                        (-rangey / 2 + j) * meshScale[1] * 1,avg_height],
                          useMaximalCoordinates=True)
            p.setGravity(0, 0, -10)
            # print(p.getNumBodies())
            # print(avg_height)
            # print(avg_score)

# run to remove heightmap
# for i in range(1,p.getNumBodies()):
#     p.removeBody(i)

height=[[[]for i in range(101)]for i in range(101)]
while True:
    # lc.handle()
    p.stepSimulation()



