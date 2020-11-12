#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Raspberry stuff
    Licencia CC by @javacasm    
    Julio de 2020
"""
import os
import subprocess
import socket
import utils
import config
import os
import urllib.request

v = '0.9'

# https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md

cmdGetTrottled = ['/opt/vc/bin/vcgencmd', 'get_throttled'] 
cmdCameraStatus = ['/opt/vc/bin/vcgencmd', 'get_camera']
cmdGetTemp = ['/opt/vc/bin/vcgencmd', 'measure_temp']
cmdDF = ['df -H | grep ', 'root ']

def init(): 
    utils.myLog('RaspiUtils ' + v)

def executeCommand(command): 
    stream = os.popen(command) 
    output = stream.read() 
    return output


def executeProcess(command, arguments): 
    process = subprocess.Popen([command, arguments], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
    stdout, stderr = process.communicate() 
    return stdout, stderr

def getTemp():
    # /opt/vc/bin/vcgencmd get_throttled
    strTemp = executeCommand(cmdGetTemp[0] + ' ' + cmdGetTemp[1]) 
    utils.myLog(strTemp) 
    return strTemp

def getThrottled(): 
    strThrotled, strError = executeProcess(cmdGetTrottled[0],cmdGetTrottled[1]) 
    strThrotled = str(strThrotled) 
    strError = str(strError)
    utils.myLog(strThrotled) 
    if strError != None:
        utils.myLog(strError) 
    return str(strThrotled)

def getDiskUsed():
    strDF = executeCommand(cmdDF[0]+config.ImagesPartition)
    df = strDF.split()
    strResult = '{} of {} free {} ocupied'.format(df[3],df[1],df[4])
    return strResult

# https://www.tutorialspoint.com/python-program-to-find-the-ip-address-of-the-client
def getHostName():
    hostname = socket.gethostname()
    utils.myLog(f"Hostname: {hostname}")
    return hostname

def getIP():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname + '.local')
    utils.myLog(f"IP Address: {ip_address}")
    return ip_address

def halt():
    utils.myLog("Shutdown! bye!")
    os.system("sudo shutdown -h now")

def reboot():
    utils.myLog("Shutdown! bye!")
    os.system("sudo reboot -f now")

# https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
# https://stackoverflow.com/questions/2792650/import-error-no-module-name-urllib2
def getPublicIP():
    fqn = os.uname()[1]
    ext_ip = urllib.request.urlopen('https://www.whatismyip.org/').read()
    utils.myLog("Host: %s " % fqn, " IP extena: %s " % ext_ip)
    return ext_ip

def camaraStatus():
    camaraStatus = executeCommand(cmdCameraStatus[0] + ' ' + cmdCameraStatus[1])
    return  camaraStatus




