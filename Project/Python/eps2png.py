# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:43:36 2022

@author: s152955
"""

import matplotlib.pyplot as plt 
from PIL import Image
import os

def list_files(dir):
    r = []
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            r.append(os.path.join(subdir, file))
            
    return r

if __name__ == "__main__":
    r = list_files("./plots")
    
    for image in r[1:]:
        img = Image.open(image);
        fig = img.convert('RGB')
        #image_png= 'logo-rgb.png'
       # fig.save(image_png, lossless = True)