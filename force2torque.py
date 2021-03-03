import math
import numpy as np

def F2Torque(leg_id,q,f):
    l1=0.0805 #abadlink
    l2=0.2 #hiplink
    l3=0.2 #kneelink
    sideSign=[-1,1,-1,1]

    s1=np.sin(q[0])
    s2=np.sin(q[1])
    s3=np.sin(q[2])

    c1=np.cos(q[0])
    c2=np.cos(q[1])
    c3=np.cos(q[2])

    c23 = c2 * c3 - s2 * s3
    s23 = s2 * c3 + c2 * s3

    J=np.zeros([3,3])
    J[0, 0] = 0
    J[0, 1] = l3 * c23 + l2 * c2
    J[0, 2] = l3 * c23
    J[1, 0] = l3 * c1 * c23 + l2 * c1 * c2 - l1 * sideSign[leg_id] * s1
    J[1, 1] = -l3 * s1 * s23 - l2 * s1 * s2
    J[1, 2] = -l3 * s1 * s23
    J[2, 0] = l3 * s1 * c23 + l2 * c2 * s1 + l1 * sideSign[leg_id] * c1
    J[2, 1] = l3 * c1 * s23 + l2 * c1 * s2
    J[2, 2] = l3 * c1 * s23

    # torque=np.zeros([3,1])
    torque=np.dot(np.array(J).T, np.array(f))
    return torque

if __name__ == '__main__':
    F = np.ones([3,4])
    f = np.zeros([3,1])
    for i in range(4):
        f = F[0:3,i]
        q=np.array([-0.2621766528125886, 1.322485268132819, -2.0386671069360265])
        tq = F2Torque(i,q,f)
        print(i,tq)
