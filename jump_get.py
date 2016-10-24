#!/usr/bin/env python
import sys
import numpy as np
import os


def get_energy(f_in):
    time_start = (9*3600+30*60)*1000
    time_end = 16*3600*1000
    delta_t = t_min*60*1000
    
    day_price = []
    
    with open(f_in, 'r') as f:
        for i in f:
            if i[:6] == ticker:
                # tmp_time = int(i[16:24])  # exe_time
                tmp_time = int(i[30:38])  # add_time
                if tmp_time >= time_start and tmp_time <= time_end:
                    # time, price, shares
                    day_price.append([tmp_time, int(i[6:16]), int(i[24:30])])
    
    bins = np.arange(time_start, time_end+delta_t, delta_t) + 0.1
    assert len(bins) == int(float(time_end-time_start)/delta_t+1)
    day_price = np.array(day_price)
    
    weighted_price = []
    
    tmp_bin = 1
    tmp_price = 0
    tmp_order = 0
    for i in day_price:
        if i[0] < bins[tmp_bin]:
            tmp_price += i[1]*i[2]
            tmp_order += i[2]
        else:
            weighted_price.append(float(tmp_price)/tmp_order/norm)
            tmp_bin += 1
            tmp_price = i[1]*i[2]
            tmp_order = i[2]
    weighted_price.append(float(tmp_price)/tmp_order/norm)
    assert len(weighted_price) == len(bins)-1
    return weighted_price

ticker = 'AAPL  '
# ticker = 'LOGI  '
# ticker = 'PRGX  '
price = []
date = []
mins = []
t_min = 5.0
norm = 10000.0
data_path = '/scratch2/users/hwf586/V2.0/stock/'
for i in sorted(os.listdir(data_path)):
    # if 'S030507' in i:
    #     break
    print i
    if os.stat(data_path+i).st_size > 0:
        tmp_energy = get_energy(data_path+i)
        tmp_date = [i[7:13]]*len(tmp_energy)
        tmp_mins = []
        for j in range(len(tmp_energy)):
            tmp_mins.append(j+1)
        price = price + tmp_energy
        date = date + tmp_date
        mins = mins + tmp_mins

f_out = open(ticker.strip()+'.dat', 'w')
for i in range(len(price)):
    f_out.write('%.10f %s %d\n' % (price[i], date[i], mins[i]))
f_out.close()
