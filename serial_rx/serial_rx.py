# -*- coding: utf-8 -*-
# use python3

import distro
from datetime import datetime
from serialcomm import SerialComm
import time

# for mock serial
from serialcomm_mock import SerialCommMock
import sys
# end of for mock serial


def GetDistro ():
    linux_name = distro.name()
    linux_ver = distro.version()

    return linux_name + ' ' + linux_ver


def SaveToMeas (line_meas):
    date_now = datetime.today()
    date_to_log = date_now.strftime("%Y-%m-%d -- %H:%M")
    with open ('master_meas.csv', 'a') as f:
        f.write(date_to_log + ',')
        f.write(line_meas + '\n')


def SaveToLog (line):
    date_now = datetime.today()
    date_to_log = date_now.strftime("%Y-%m-%d -- %H:%M")
    with open ('master.log', 'a') as f:
        f.write(date_to_log + ', ')
        f.write(line + '\n')
        

def SerialCb (dataread):
    # strip the end of line
    srx = dataread.rstrip('\n')
    srx = srx.rstrip('\r')
    if srx.startswith('last_10_all'):
        # check csv
        srx_list = srx.split(',')
        if len(srx_list) != 6:
            return

        srx_comma = srx.find(',') + 1
        srx = srx[srx_comma:]
        SaveToMeas(srx)

    elif srx.startswith('uptime hours'):
        # log the uptime
        SaveToLog(srx)

    else:
        pass
    
            
if __name__ == "__main__":
    serial_cls = SerialComm
    if len(sys.argv) >= 2 and sys.argv[1] == 'mock':
        serial_cls = SerialCommMock
        print('argv len: ' + str(len(sys.argv)))
        
    local_distro = GetDistro()
    print('Distro: ' + local_distro)
    SaveToLog(local_distro)

    # open serial port
    local_distro = distro.name()

    if local_distro == 'Slackware':
        ## for slack machine w/adapter
        s_port = serial_cls(SerialCb, '/dev/ttyUSB0')

    elif local_distro == 'Raspbian GNU/Linux':
        ## for rpi
        s_port = serial_cls(SerialCb, '/dev/serial0')

    else:
        ## distro unknown???
        print("distro unknown, port not open!!!")        
        SaveToLog("distro unknown, port not open!!!")
        
    if s_port.port_open == False:
        print("Serial port not found!!!")
        SaveToLog("Serial port not found!!!")

    else:
        print("Serial found, getting uptime")
        SaveToLog("Serial found, getting uptime")
        s_port.Write("\r\n")
        time.sleep(0.1)
        s_port.Write("\r\n")
        time.sleep(0.1)
        s_port.Write("uptime\r\n")        

        # loop always, wait for comms callback
        # loop_always = True
        # while loop_always:
        #     time.sleep(0.1)
        #     if s_port.port_open == False:
        #         print("port closed! reboot")        
        #         SaveToLog("port closed! reboot")
        #         s_port.Close()
        #         loop_always = False

        ## serialmock answers
        # answer for uptime
        SerialCb("uptime hours 60000\r\n")
        # ten minutes meas
        SerialCb("last_10_all,2,0,0,0,2\r\n")
        
