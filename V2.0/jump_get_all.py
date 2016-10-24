#!/usr/bin/env python
import numpy as np
import os
import sys


def get_energy(f_in):
    time_start = (9*3600+30*60)*1000
    time_end = 16*3600*1000
    delta_t = t_min*60*1000
    
    day_price = []
    
    with open(f_in, 'r') as f:
        for i in f:
            if i[:6] == ticker:
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
    
    if len(day_price) > 0:
        inds = np.digitize(day_price[:,0], bins)
    else:
        return [-1.0]*(len(bins)-1)
    for i in range(len(day_price)):
        tmp = day_price[i]
        if inds[i] <= len(weighted_price):
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
for tmp_ticker in ticker_all:
    if os.path.exists('/scratch2/users/hwf586/V2.0/ticker/'+tmp_ticker.strip()+'.dat'):
        pass
    else:
        ticker = tmp_ticker
        f_out = open('/scratch2/users/hwf586/V2.0/ticker/'+tmp_ticker.strip()+'.dat', 'w')

        if ticker == '':
            sys.exit()
        
        price = []
        date = []
        mins = []
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
                price = price + tmp_energy
                date = date + tmp_date
                mins = mins + tmp_mins
        
        for i in range(len(price)):
            f_out.write('%.10f %s %d\n' % (price[i], date[i], mins[i]))
        f_out.close()
