#!/usr/bin/env python

import zipfile
import sys
import csv

time_sec = ''
time_mili = ''
f_out = csv.writer(open(sys.argv[2].strip()+'.csv', 'w'), delimiter=',')
z = zipfile.ZipFile(sys.argv[1], 'r')
buff = {}
buff['RefNum'] = []


def check_time(tmp_time):
    if tmp_time % 100000 == 0:
        print tmp_time, len(buff['RefNum'])
    if tmp_time > (10*3600+30*60)*1000 and tmp_time < (15*3600*1000):
        return True
    else:
        return False

for zinfo in z.infolist():
    for i in z.open(zinfo):
        if check_time(int(i[:8])):
            # for Add order without NPID
            if i[8] == 'A':
                tmp = i[:-1]
                assert len(tmp) == 42
                if tmp[25:31] == sys.argv[2]:
                    buff['RefNum'].append(tmp[9:18])
                    f_out.writerow([tmp])
    
            # for Executed order
            if i[8] == 'E':
                tmp = i[:-1]
                assert len(tmp) == 33
                if tmp[9:18] in buff['RefNum']:
                    buff['RefNum'].remove(tmp[9:18])
                    f_out.writerow([tmp])
    
            # for Canceled order
            if i[8] == 'X':
                tmp = i[:-1]
                assert len(tmp) == 24
                if tmp[9:18] in buff['RefNum']:
                    buff['RefNum'].remove(tmp[9:18])
