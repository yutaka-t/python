# -*- coding:utf-8 -*-

import cv2

import numpy as np

# PIC = r"pic01.jpg"
# PIC = r"C:\Users\yutak\Dropbox\Camera Uploads\2018-10-27 15.36.24.jpg"
PIC = 'shinki.jpg'

try:
    img = cv2.imread(PIC, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError('ファイルが見つかりません')

    ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('sample02', dst)

    ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('sample03', dst)

    ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
    cv2.imshow('sample04', dst)

    ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    cv2.imshow('sample05', dst)

    ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
    cv2.imshow('sample06', dst)



    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
