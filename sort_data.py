#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt

time_start = (10*3600+30*60)*1000
time_end = 15*3600*1000
t_min = 5
delta_t = t_min*60*1000

order = {}
price = []
with open(sys.argv[1], 'r') as f:
    for i in f:
        if i[8] == 'A':
            order[i[9:18]] = float(i[31:41])/10000
        if i[8] == 'E':
            price.append([int(i[:8]), order[i[9:18]], int(i[18:24])])

bins = np.arange(time_start, time_end+delta_t, delta_t) + 0.1
assert len(bins) == int(float(time_end-time_start)/delta_t+1)
price = np.array(price)

weighted_price = []

tmp_bin = 1
tmp_price = 0
tmp_order = 0
for i in price:
    if i[0] < bins[tmp_bin]:
        tmp_price += i[1]*i[2]
        tmp_order += i[2]
    else:
        weighted_price.append(float(tmp_price)/tmp_order)
        tmp_bin += 1
        tmp_order = i[1]
        tmp_price = i[2]
weighted_price.append(float(tmp_price)/tmp_order)
assert len(weighted_price) == len(bins)-1

price = weighted_price
price[20] = 61

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


L_stat = []
for i in range(K, len(price)):
    iVol = 0
    for j in range(i-K+2, i):
        iVol += np.abs(np.log(price[j])/price[j-1])*np.abs(np.log(price[j-1])/price[j-2])
    iVol = np.sqrt(iVol/(K-2))
    L_stat.append(np.log(price[i]/price[i-1])/iVol)

print L_stat
print G1*Sn+Cn


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(range(len(price)), price, 'ro')

ax2 = ax1.twinx()
ax2.plot(np.array(range(len(L_stat)))+10, L_stat, 'g.')
plt.show()
