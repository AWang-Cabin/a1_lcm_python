import numpy as np
import math
import csv
import pandas as pd
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt

# compute traversability with height and map sizes

def heightmap2score(height,x_size,y_size):
    # score wieght
    w_sd=60.
    w_sl=30.
    w_max=10.
    w_min=10.

    score=np.zeros((x_size,y_size))
    for i in range(x_size):
        for j in range(y_size):

            if i>=1 and j>=1 and i<x_size-1 and j<y_size-1:
                slope,sum=0.,0.
                hmax= height[i][j]
                hmin=height[i][j]
                tmpmap=np.zeros(9)
                k=0
                for m in [i-1,i,i+1]:
                    for n in [j-1,j,j+1]:
                        # // slope
                        if not(m==i and n==j):
                            slope=abs((height[i][j]-height[m][n])/np.sqrt(pow((i-m),2)+pow((j-n),2)))+slope
                         # //max
                        if height[m][n]>hmax:
                            hmax=height[m][n]
                         # //min
                        if height[m][n]<hmin:
                            hmin=height[m][n]
                        #   sum
                        sum=sum+height[m][n]
                        tmpmap[k]=height[m][n]#暂存周围区域的高度值
                        k+=1

                # //标准差
                mean=sum/9.
                sd_sum=0.
                for l in range(9):
                    sd_sum=sd_sum+pow((tmpmap[l]-mean),2)
                sd=np.sqrt(sd_sum/9.)
                # //平均斜率
                slope=slope/8.
                # //traversability map
                score[i][j] = w_sd*sd + w_sl*slope + w_max*(hmax-height[i][j]) + w_min*(height[i][j]-hmin)

            elif i==0 or j==0 or i==x_size-1 or j==y_size-1:
                score[i][j] = 0.

            # if i==1 and j==10:
            #     print(hmax)
            #     print(hmin)
            #     print(sd)
            #     print(slope)
            #     print(height[i][j])
            #     print(score[i][j])
    return score


if __name__ == '__main__':
    heightdata = pd.read_csv('demo.csv', sep=' ', header=None)
    # with open('heightmap22.txt','r') as file:
    #     heightdata = []
    #     for i in range(101):
    #         row=[]
    #         for j in range(101):
    #             line = file.readline()
    #             row.append(float(line))
    #         heightdata.append(row)
    heightdata=np.array(heightdata)
    print(heightdata.shape)

    _x_size,_y_size=500,200
    scoredata=heightmap2score(heightdata,_x_size,_y_size)
    sum=0.
    # list=[]
    for i in range(_x_size):
        for j in range(_y_size):
            # list.append(scoredata[i][j])
            print(scoredata[i][j],end=" ")
            # sum=sum+scoredata[i][j]
        print(" ")
    # print(sum)

    # fig=plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # for x in range(0,100,1):
    #     y=np.arange(0.,100.,1)
    #     ax.scatter(x, y, scoredata[x],color='b')
    # plt.show()