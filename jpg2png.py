# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 14:45:54 2020

@author: celia
"""

from PIL import Image
import glob

for file in glob.glob('*.png'):
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    rgb_im.save(file.replace('png', 'jpg'), quality = 95)