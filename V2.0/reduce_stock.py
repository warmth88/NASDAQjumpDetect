#!/usr/bin/env python
# broken trade message not excluded!
# output order: ticker, price, exe_time, shares

import zipfile
import os
import time
import pysftp


# Skip ones completed
reduce_list = []
with open('reduce_list.dat', 'r') as f:
    for i in f:
        reduce_list.append(i.split()[0])
f_reduce_list = open('reduce_list.dat', 'a')

# location of orignal data files
with pysftp.Connection('aimchapmannas.kellogg.northwestern.edu',
                        username='hwf586', password='just-many-earth-printed') as sftp:
    path_in = './itchfilesarchive_v2/'
    with sftp.cd('huanxin'):             # temporarily chdir to public
        #sftp.get('remote_file')         # get a remote file
        file_list = sftp.listdir(path_in)
        data_list = []
        for i in file_list:
            if i[5:7] == '07' and (i not in reduce_list):
                data_list.append(i)


        for i in data_list:
            start = time.time()
            path_exed = '/scratch2/users/hwf586/V2.0/exe/'
            path_out = '/scratch2/users/hwf586/V2.0/stock/'
            f_out = open(path_out+'stock_'+i[:-4]+'.dat', 'w')
        
            # get all executed orders ref number and executed shares
            with open(path_exed+'Exe_'+i[:-4]+'.dat', 'r') as f:
                id_list = {}
                for j in f:
                    if j[8] == 'E':
                        try:
                            id_list[int(j[9:18])].append(j[:8]+j[18:24])
                        except:
                            try:
                                id_list[int(j[9:18])] = [j[:8]+j[18:24]]
                            except:
                                print j
                    else:
                        print 'Broken Trade: ', j

            path_tmp = '/scratch2/users/hwf586/V2.0/'        
            sftp.get(path_in+i, path_tmp+i)
            while not os.path.exists(path_tmp+i):
                time.wait(60)
            assert sftp.lstat(path_in+i).st_size == os.stat(path_tmp+i).st_size
            z = zipfile.ZipFile(path_tmp+i)
            for zinfo in z.infolist():
                for j in z.open(zinfo):
                    try:
                        if j[8] == 'A':
                            ref = int(j[9:18])
                            try:
                                tmp = id_list[ref]
                                for k in id_list[ref]:
                                    f_out.write('%s%s%s\n' % (j[25:31]+j[31:41], k, j[:8]))
                                del id_list[ref]
                            except:
                                pass
                    except:
                        pass
            end = time.time()
            print '%s %.2f mins' % (i, (end-start)/60.0)
            os.remove(path_tmp+i)
            f_reduce_list.write('%s %.2f mins\n' % (i, (end-start)/60.0))
        f_reduce_list.close()
