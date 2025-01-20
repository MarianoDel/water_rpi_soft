# -*- coding: utf-8 -*-
# use python3

import distro
from datetime import datetime, date, timedelta
import sys
import os
# import time

#### files in use
meas_file_str = 'master_meas.csv'
meas_file_path_str = '../serial_rx/'
bkp_dir_path_srt = '../../'

def SaveToLog (line):
    date_now = datetime.today()
    date_to_log = date_now.strftime("%Y-%m-%d -- %H:%M")
    with open ('backup.log', 'a') as f:
        f.write(date_to_log + ', ')
        f.write(line + '\n')


def CheckCreateDir (dir_name):
    new_dir_backup_str = '../../' + dir_name
    if os.path.exists( new_dir_backup_str ) != True:
        print('dir ' + new_dir_backup_str + ' needs to be created')
        os.mkdir( new_dir_backup_str )
                

def CreateDummyFileOnDirectory (dir_name, inner_date):
    new_dir_backup_str = '../../' + dir_name
    if os.path.exists( new_dir_backup_str ) != True:
        print('dir ' + new_dir_backup_str + ' was not previusly created! Aborting...')
        sys.exit()

    with open (new_dir_backup_str + '/' + 'master_meas.csv', 'w') as f:
        for x in range (24):
            for y in range (6):
                f.write(inner_date + ' -- ' + f"{x:02d}" + ':' + f"{y}5,1,0,0,0,1\n")

    
if __name__ == "__main__":
    # check args for operation
    if len(sys.argv) != 3:
        print('use this script with format YYYYMMDD: init_date end_date')
        sys.exit()

    # get the dates
    init_date_str = sys.argv[1]
    end_date_str = sys.argv[2]
    # print('first date: ' + init_date_str + ' end date: ' + end_date_str)
    init_date_num = 0
    end_date_num = 0
    try:
        init_date_num = int(init_date_str)
        end_date_num = int(end_date_str)
    except:
        print('wrong dates format')
        sys.exit()

    if init_date_num > end_date_num:
        print('end date must be equal or greater then init date')
        sys.exit()
        
    # convert to date and check days qtty
    init_date = date.fromisoformat(init_date_str)
    end_date = date.fromisoformat(end_date_str)

    date_delta = end_date - init_date
    print('days between dates: ' + str(date_delta.days))

    if date_delta.days > 100:
        print('no more than hundred days can be created by this script')
        sys.exit()

    # create dummys directories
    for d in range(date_delta.days + 1):
        days_delta = timedelta(days=d)
        date_to_log = init_date + days_delta
        # print(date_to_log.strftime("%Y%m%d"))
        CheckCreateDir(date_to_log.strftime("%Y%m%d"))
        CreateDummyFileOnDirectory(date_to_log.strftime("%Y%m%d"), date_to_log.strftime("%Y-%m-%d"))
        

        
