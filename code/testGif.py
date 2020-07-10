#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" generación de ficheros gif a partir de imágenes
    Licencia CC by @javacasm    
    Julio de 2020
"""

import os
import glob
import imageio


## Documentación sobre glob https://docs.python.org/3/library/glob.html#glob.glob
## Documentación sobre imagio https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python



def getFileList(dir, filtro):
    return sorted(glob.glob(os.path.join(dir, filtro)))

def getFileList2(dir, extension):
    imageFiles = []
    for file_name in os.listdir(dir):
        if file_name.endswith(extension):
            file_path = os.path.join(dir, file_name)
            imageFiles.append(file_path)
            
    return sorted(imageFiles)

def createGif(imagesDir, filter, gifFile,fps):
    imageFiles = getFileList(imagesDir, filter)
    images = []
    for imageFile in imageFiles:
        images.append(imageio.imread(imageFile))
    imageio.mimsave(gifFile, images, fps = fps)



imagesDir = '/home/javacasm/Descargas/timeLapse/ajo'

filtro = 'image20200709-???[1,3,5,7,9]??.jpg'

ficheroGif = './movie3.gif'

gif_file = os.path.join(imagesDir, ficheroGif)

createGif(imagesDir, filtro, gif_file, 10)


