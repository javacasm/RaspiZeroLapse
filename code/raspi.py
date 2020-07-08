
import os
import subprocess

import utils

v = '0.2'

cmdGetTrottled = ['/opt/vc/bin/vcgencmd', 'get_throttled']
cmdGetTemp = ['/opt/vc/bin/vcgencmd', 'measure_temp']

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
    strThrotled, strError = executeProcess(cmdGetTrottled[0],cmdGetTrottled[1)]
    utils.myLog(strThrotled)
    if strError != None:
        utils.myLog(strError)
    return strThrotled