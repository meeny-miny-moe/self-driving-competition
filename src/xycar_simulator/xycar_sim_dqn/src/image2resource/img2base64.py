#!/usr/bin/env python

import base64
from PIL import Image
import numpy as np
import cv2

#f = open("logo.txt", "w")
#img = cv2.imread('logo.png')
#_, im_arr = cv2.imencode('.png', img)
#im_bytes = im_arr.tobytes()
#im_b64 = base64.b64encode(im_bytes)
#f.write(im_b64.decode("utf-8"))
#f.close()

#f = open("car.txt", "w")
#img = cv2.imread('car.png')
#_, im_arr = cv2.imencode('.png', img)
#im_bytes = im_arr.tobytes()
#im_b64 = base64.b64encode(im_bytes)
#f.write(im_b64.decode("utf-8"))
#f.close()

f = open("logo.txt", "w")
with open('./logo.png', 'rb') as img:
    base64_string = base64.b64encode(img.read())
    f.write(base64_string.decode("utf-8"))
f.close()

f = open("car.txt", "w")
with open('./car.png', 'rb') as img:
    base64_string = base64.b64encode(img.read())
    f.write(base64_string.decode("utf-8"))
f.close()
