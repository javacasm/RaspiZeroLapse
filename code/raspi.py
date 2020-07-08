
import os
import subprocess

import utils

cmdGetTemp = ['opt/vc/bin/vcgencmd', 'get_throttled']

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

