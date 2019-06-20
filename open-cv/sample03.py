# -*- coding:utf-8 -*-

import cv2

import numpy as np

PIC = r"pic01.jpg"
# PIC = r"C:\Users\yutak\Dropbox\Camera Uploads\2018-10-27 15.36.24.jpg"

try:
    img = cv2.imread(PIC, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError('ファイルが見つかりません')

    blue, green, red = cv2.split(img)
    cv2.imshow('blue', blue)
    cv2.imshow('green', green)
    cv2.imshow('red', red)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
