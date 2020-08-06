#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" generación de ficheros gif a partir de imágenes
    Licencia CC by @javacasm    
    Julio de 2020
"""

import os
import glob
import imageio
import utils


## Documentación sobre glob https://docs.python.org/3/library/glob.html#glob.glob
## Documentación sobre imagio https://imageio.readthedocs.io/en/stable/sec_gettingstarted.html
## imageio y gifs https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python



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
    cursors = ['|','\\','-','/','-']
    images = []
    counter = 0
    cursor = 0
    for imageFile in imageFiles:
        images.append(imageio.imread(imageFile))
        if counter%10 == 0 :
            print(' {} {} of {} images'.format(cursors[cursor%len(cursors)],counter,len(imageFiles)),end = '\r')
            cursor += 1
        counter += 1
    print(' Saving gif with {} images'.format(len(imageFiles)),end = '\r')
    imageio.mimsave(gifFile, images, fps = fps)
    print('Gif file {} with {} images'.format(gifFile, len(imageFiles)))
    return gifFile



imagesDir = '/home/javacasm/Descargas/timeLapse/tormenta/'

filtro = 'image2020071*.jpg'

ficheroGif = 'tormenta.gif'

gif_file = os.path.join(imagesDir, ficheroGif)

finalfile = createGif(imagesDir, filtro, gif_file, 10)


