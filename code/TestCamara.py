#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Test of cámara functionality
    Licencia CC by @javacasm    
    Julio de 2020
 """


import camara
import utils
from time import sleep

v = '0.7'

print('Camara version: '+ camara.v)

camera = camara.initCamera() # creamos el objeto camara

def testISO():
    for iso in range(100,900,100):
        message = 'ISO:' + str(iso)
        print(message)
        camara.addText(message)
        camara.setIso(iso)
        camara.getImage()

def testImage():
    for i in range(1, 3):
        camara.addDate()
        camara.getImage()
        sleep(5)

def testImageNight():
    for i in range(1, 3):
        camara.addDateNight()
        camara.getImageNight()
        sleep(5)


def testResolution():
   camara.resolucionHD()
   mess = 'HD:' + str(camara.camera.resolution)
   utils.myLog(mess)
   camara.addText(mess)
   camara.getImage(fileName = 'imageHD.jpg')

   camara.resolucionV1()
   mess = 'V1D:' + str(camara.camera.resolution)
   utils.myLog(mess)
   camara.addText(mess)
   camara.getImage(fileName = 'imageV1D.jpg')

   camara.resolucionMD()
   mess = 'MD:' + str(camara.camera.resolution)
   utils.myLog(mess)
   camara.addText(mess)
   camara.getImage(fileName = 'imageMD.jpg')

   camara.resolucionLD()
   mess = 'LD:' + str(camara.camera.resolution) 
   utils.myLog(mess)
   camara.addText(mess)
   camara.getImage(fileName = 'imageLD.jpg')

testResolution()
