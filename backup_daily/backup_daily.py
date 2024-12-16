# -*- coding: utf-8 -*-
# use python3

import distro
from datetime import datetime
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
        

def GetDirBackup ():
    # get the date
    date_now = datetime.today()
    date_day = date_now.strftime("%Y%m%d")
    return date_day

    
def CreateDirBackup ():
    # get the date
    date_day = GetDirBackup()
    # check or create dir
    CheckCreateDir(date_day)
    return date_day


def CheckAllFiles ():
    # check for meas file
    meas_str = meas_file_path_str + meas_file_str
    if os.path.isfile( meas_str ) == True:
        print('meas file finded in: ' + meas_str)
    else:
        print('meas file: ' + meas_str + ' not finded!!!')
            
    # check for backup dir
    dir_bkp_str = GetDirBackup()
    dir_bkp_str = bkp_dir_path_srt + dir_bkp_str
    if os.path.exists( dir_bkp_str ) == True:
        print('backup dir finded in: ' + dir_bkp_str)
        # check for meas backup file
        bkpf_str = dir_bkp_str + '/' + meas_file_str
        if os.path.isfile( bkpf_str ) == True:
            print('backup file already in: ' + bkpf_str)
        else:
            print('backup file: ' + bkpf_str + ' needs to be created!!!')
            
    else:
        print('backup dir: ' + dir_bkp_str + ' needs to be created!!!')
    

def CopyPulsesFile ():
    # find pulses file
    meas_f_str = meas_file_path_str + meas_file_str
    dir_bkp_str = GetDirBackup()
    dir_bkp_str = bkp_dir_path_srt + dir_bkp_str
    bkp_file_str = dir_bkp_str + '/' + meas_file_str
    if os.path.exists( meas_f_str ) == True and \
       os.path.isfile( meas_f_str ) == True:
        print('pulses file finded')

        if os.path.isfile( bkp_file_str ) == True:
            err_str = 'destination file: ' + bkp_file_str + ' already exists, abort ops'
            print(err_str)
            SaveToLog(err_str)
            return
        else:
            err_str = 'destination file: ' + bkp_file_str + ' not present'
            print(err_str)
            SaveToLog(err_str)            

        # copy meas file
        try:
            os.system('cp -f ' + meas_f_str + ' ' + dir_bkp_str)
        except:
            print('error in copy meas file')
            SaveToLog('error in copy meas file')
            return

        if os.path.isfile( bkp_file_str ) == True:
            print('copy backup sucess!')
            SaveToLog('copy backup sucess!')
        else:
            err_str = 'error in backup file: ' + bkp_file_str
            print(err_str)
            SaveToLog(err_str)
            return
        
        # zero out meas file
        try:
            os.system('cat /dev/null > ' + meas_f_str)
        except:
            print('error zeroing meas file')
            SaveToLog('error zeroing meas file')
            return

        if os.path.getsize( meas_f_str ) == 0:
            print('zero out meas sucess!')
            SaveToLog('zero out meas sucess!')
        else:
            err_str = 'error zero out backup file!'
            print(err_str)
            SaveToLog(err_str)
        
    else:
        print('pulses file not finded!' + ' ' + meas_f_str)
        SaveToLog('pulses file not finded!' + ' ' + meas_f_str)
        
    
if __name__ == "__main__":
    # check args for operation
    if len(sys.argv) != 2:
        print('use this script with the following options: check backup')
        sys.exit()
    
    if sys.argv[1] == 'check':
        print('argv len: ' + str(len(sys.argv)) + ' ' + sys.argv[1])
        CheckAllFiles ()

    elif sys.argv[1] == 'backup':
        print('argv len: ' + str(len(sys.argv)) + ' ' + sys.argv[1])
        CreateDirBackup()
        CopyPulsesFile()
        
    else:
        print('use this script with the following options: check backup')
    # local_distro = GetDistro()
    # print('Distro: ' + local_distro)
    # SaveToLog(local_distro)

    # # open serial port
    # local_distro = distro.name()

        
