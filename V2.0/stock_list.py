#!/usr/bin/env python
import os
path = '/scratch2/users/hwf586/V2.0/stock/'

ticker = {}
for i in os.listdir(path):
    with open(path+i, 'r') as f_in:
        for j in f_in:
            tmp = j[:6]
            ticker[tmp] = 1
    print i, ' done', len(ticker)

with open('all_ticker07.dat', 'w') as f_out:
    for i in ticker.keys():
        f_out.write('%s\n' % (i))
