#!/usr/bin/env python
import zipfile
import os
import time
import pysftp


# Skip ones completed
exe_list = []
with open('exe_list.dat', 'r') as f:
    for i in f:
        exe_list.append(i.split()[0])
f_exe_list = open('exe_list.dat', 'a')


with pysftp.Connection('aimchapmannas.kellogg.northwestern.edu',
                        username='hwf586', password='just-many-earth-printed') as sftp:
    path_in = './itchfilesarchive_v3/'
    with sftp.cd('huanxin'):             # temporarily chdir to public
        file_list = sftp.listdir(path_in)
        data_list = []
        for i in file_list:
            if i[5:7] == '08' and (i not in exe_list) and 'zip' in i:
                data_list.append(i)
        
        for i in data_list:
            start = time.time()
            path_tmp = '/scratch2/users/hwf586/V3.0/'
            path_out = '/scratch2/users/hwf586/V3.0/exe/'
            sftp.get(path_in+i, path_tmp+i)
            while not os.path.exists(path_tmp+i):
                time.wait(60)
            assert sftp.lstat(path_in+i).st_size == os.stat(path_tmp+i).st_size
            f_out = open(path_out+'Exe_'+i[:-4]+'.dat', 'w')
            z = zipfile.ZipFile(path_tmp+i)
            for zinfo in z.infolist():
                for j in z.open(zinfo):
                    try:
                        if j[0] == 'T':
                            time_sec = j[:-1]
                        if j[0] == 'M':
                            time_mili = j[:-1]
                        if j[0] == 'E' or j[0] == 'C' or j[0] == 'B':
                            f_out.write('%s %s\n' % (j[:-1], time_sec+time_mili))
                    except:
                        print 'yes'
            end = time.time()
            print '%s %.2f mins' % (i, (end-start)/60.0)
            os.remove(path_tmp+i)
            f_exe_list.write('%s %.2f mins\n' % (i, (end-start)/60.0))
        f_exe_list.close()
