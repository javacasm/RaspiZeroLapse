#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Test of cámara functionality
    Licencia CC by @javacasm    
    Julio de 2020
 """


import camara
from time import sleep

camera = camara.initCamera() # creamos el objeto camara

for i in range(1, 3):
    camara.addDate()
    camara.getImage()
    sleep(5)