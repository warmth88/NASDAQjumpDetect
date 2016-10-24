#!/usr/bin/env python

import pysftp

with pysftp.Connection('aimchapmannas.kellogg.northwestern.edu',
                        username='hwf586', password='just-many-earth-printed') as sftp:
    with sftp.cd('huanxin'):             # temporarily chdir to public
        #sftp.get('remote_file')         # get a remote file
        file_list = sftp.listdir('./itchfilesarchive_v2/')
