import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import math as math
plt.style.use('ggplot')

PRIM = 1000000

# n = integrating dimensions
n = 2

def f1(x,z):
    return x*z*np.exp(-3*x)*np.sin(x*z)

xlimMin = -1
xlimMax = 3
zlimMin = 0
zlimMax = 3


x = np.linspace(xlimMin, xlimMax, 100)
z = np.linspace(zlimMin, zlimMax, 100)
ylimMin = 0
ylimMax = 0
for i in range(0,len(x)):
    for ii in range(0,len(z)):
        val = f1(x[i],z[ii])
        if val < ylimMin:
            ylimMin = val
        if val > ylimMax:
            ylimMax = val



pts = np.zeros([PRIM,n +1])

pts[0:,0] = np.random.uniform(xlimMin,xlimMax,(PRIM))
pts[0:,1] = np.random.uniform(ylimMin,ylimMax,(PRIM))
pts[0:,2] = np.random.uniform(zlimMin,zlimMax,(PRIM))


posCounts = float(0)
negCounts = float(0)
negPRIM = float(0)
for i in range(0,PRIM):
    x = pts[i,0]
    y = pts[i, 1]
    z = pts[i, 2]
    funY = f1(pts[i,0],pts[i, 2])
    if y <=  funY and y >= 0:#*f2(pts[i, 2]):   
        posCounts = posCounts + 1
    if y >=  funY and y < 0:
        negCounts = negCounts + 1
    if y < 0:
        negPRIM = negPRIM +1


        #ylimMax fissy here
totPosVolume = (xlimMax - xlimMin)*(ylimMax)*(zlimMax - zlimMin)

totNegVolume = abs(ylimMin)*(xlimMax - xlimMin)*(zlimMax - zlimMin)



#Ratio of total volume
Apos = (posCounts/(PRIM-negPRIM)) * totPosVolume
if negPRIM != 0: 
    Aneg = (negCounts/negPRIM) * totNegVolume 
else:
    Aneg = 0


#plt.scatter(pts[:, 0], pts[:, 1])
#plt.xlim([xlimMin,xlimMax])
#plt.ylim([ylimMin, ylimMax]);
#x = np.linspace(xlimMin, xlimMax, 100)
#y = np.linspace(ylimMin, ylimMax, 100)
#plt.plot(x, f1(x),linewidth=3.0);
#plt.plot(x, np.zeros(100),'r--',linewidth=2.0);
#plt.plot(np.zeros(100), y,'r--',linewidth=2.0);
print('--------')
print('Pos: ' + str(Apos))
print('Neg: ' + str(Aneg))
print('Estimated: ' + str(Apos - Aneg))
#plt.show()

