"""

Usamos psutil

"""

v = '0.4'

import  raspi
import utils

cuantos = raspi.checkPythonProcessRunning('raspiCarbot.py')

utils.myLog('Hay {} instancias'.format(cuantos))



