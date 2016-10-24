#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

ticker = 'AAPL  '
# ticker = 'LOGI  '
price = []
date = []
mins = []
with open(ticker.strip()+'.dat', 'r') as f:
    for i in f:
        tmp = i.split()
        price.append(float(tmp[0]))
        date.append(tmp[1])
        mins.append(int(tmp[2]))

t_min = 5.0
# set constatns
c = np.sqrt(2/np.pi)
n = len(price)
k = np.sqrt(2*np.log(n))
Sn = 1./(c*k)
Cn = k/c-(np.log(np.pi)+np.log(np.log(n)))/(2*c*k)
G1 = 4.6001

# set window size
K = int(np.ceil(np.sqrt(1440.0/t_min*252)))
if len(price) < K:
    K = 10
    print '%d data points, need at least %d, use 10' % (len(price), K)
print K


L_stat = []
for i in range(K, len(price)):
    iVol = 0
    for j in range(i-K+2, i):
        iVol += np.abs(np.log(price[j]/price[j-1]))*np.abs(np.log(price[j-1]/price[j-2]))
    iVol = np.sqrt(iVol/(K-2))
    L_stat.append(np.log(price[i]/price[i-1])/iVol)

threshold = G1*Sn+Cn
print len(L_stat), len(price)

cited = []
cited_plot = []
falseAlarm = []
falseAlarm_plot = []
for i in range(len(price)):
    if i < K:
        pass
    if abs(L_stat[i-K]) > threshold:
        # persist for 3 time intervals
        flag = True
        for j in range(3):
            if abs(L_stat[i-K+1+j]) > threshold:
                flag = False
        if flag:
            if (12<mins[i]<=66):
                cited.append(i)
                cited_plot.append(L_stat[i-K])
            else:
                falseAlarm.append(i)
                falseAlarm_plot.append(L_stat[i-K])
print len(cited)

for i in falseAlarm:
    print date[i], mins[i]


fig = plt.figure()

ax1 = fig.add_subplot(111)
date_tmp = date[0]
x_tmp = []
y_tmp = []
flag = 1
for i in range(len(price)):
    x_tmp.append(i)
    y_tmp.append(price[i])
    if date[i] != date_tmp:
        if flag > 0:
            ax1.plot(x_tmp, y_tmp, 'b-')
            flag *= -1
        else:
            ax1.plot(x_tmp, y_tmp, 'c-')
            flag *= -1
        x_tmp = [i]
        y_tmp = [price[i]]
        date_tmp = date[i]

ax2 = ax1.twinx()
ax2.plot(np.array(range(len(L_stat)))+K, L_stat, 'g.')

ax2.plot(cited, cited_plot, 'ro')
ax2.plot(falseAlarm, falseAlarm_plot, 'r.')
fig.savefig('AAPL.pdf', dpi=300)
plt.show()
