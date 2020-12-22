#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Test of Raspi functionality
    Licencia CC by @javacasm    
    Julio de 2020
 """

import raspi

v = '0.4'

raspi.init()

temp = raspi.getTemp()

print('Temperatura: ' + temp)

throttled = raspi.getThrottled()

print('Throtted: ' + throttled)

df = raspi.getDiskUsed()

print('Disk Used: ' + df)

ip = raspi.getIP()
print ('IP:'+ip)

hostname = raspi.getHostName()
print ('Hostname:' + hostname )

# print('Reboot!')
# raspi.reboot()

# ipPublica = raspi.getPublicIP()
# print('IP Pública: ' + ipPublica)

camaraStatus = raspi.camaraStatus()
print('Camara Status: ' + camaraStatus)
