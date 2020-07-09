#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" http utils
    Licencia CC by @javacasm    
    Julio de 2020
    original @inopya https://github.com/inopya/mini-tierra    
"""
import requests

v = '1.1'

def get_url(url):
    '''
    Funcion de apoyo a la recogida de telegramas,
    Recoge el contenido desde la url de telegram
    '''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
