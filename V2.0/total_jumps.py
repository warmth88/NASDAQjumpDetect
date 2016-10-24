#!/usr/bin/env python
import numpy as np
import os
import sys


def get_energy(f_in):
    time_start = (9*3600+30*60)*1000
    time_end = 16*3600*1000
    delta_t = t_min*60*1000
    
    day_price = {}
    
    with open(f_in, 'r') as f:
        for i in f:
            if i[:6] == ticker:
            ticker = i[:6]
                tmp_time = int(i[16:24])  # exe_time
                # tmp_time = int(i[30:38])  # add_time
                if tmp_time >= time_start and tmp_time <= time_end:
                    # time, price, shares
                    day_price.append([tmp_time, int(i[6:16]), int(i[24:30])])
    
    bins = np.arange(time_start, time_end, delta_t)
    bins = np.append(bins, [time_end])
    assert len(bins) == int(float(time_end-time_start)/delta_t+1)
    # bins_center = [(a+b)/2 for a, b in zip(bins[::2], bins[1::2])]
    weighted_price = [0.0]*(len(bins)-1)
    weights = [0]*(len(bins)-1)

    day_price = np.array(day_price)
    
    inds = np.digitize(day_price[:,0], bins)
    for i in range(len(day_price)):
        tmp = day_price[i]
        weighted_price[inds[i]-1] += tmp[1]*tmp[2]
        weights[inds[i]-1] += tmp[2]
    for i in range(len(weights)):
        if abs(weights[i]) > 1e-6:
            weighted_price[i] = float(weighted_price[i])/weights[i]/norm
        else:
            weighted_price[i] = -1.0  # make missing data negative and clean it later
    return weighted_price


ticker_all = []
with open('all_ticker07.dat', 'r') as f_ticker:
    for i in f_ticker:
        ticker_all.append(i[:-1])


ticker = ''
for i in ticker_all:
    if os.path.exists('./ticker/'+i.strip()+'.dat'):
        pass
    else:
        ticker = i
        f_out = open('./ticker/'+i.strip()+'.dat', 'w')
        break

if ticker == '':
    sys.exit()

t_min = 5.0
norm = 10000.0
data_path = '/scratch2/users/hwf586/V2.0/stock/'
print ticker
for i in sorted(os.listdir(data_path)):
    # if 'S010407' in i:
    #     break
    # print i
    if os.stat(data_path+i).st_size > 0:
        tmp_energy = get_energy(data_path+i)
        tmp_date = [i[7:13]]*len(tmp_energy)
        tmp_mins = []
        for j in range(len(tmp_energy)):
            tmp_mins.append(j+1)
        for i in range(len(tmp_energy)):
            f_out.write('%.10f %s %d\n' % (tmp_energy[i], tmp_date[i], tmp_mins[i]))

f_out.close()
