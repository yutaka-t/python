# -*- coding:utf-8 -*-

import cv2

import numpy as np

PIC = r"pic01.jpg"
# PIC = r"C:\Users\yutak\Dropbox\Camera Uploads\2018-10-27 15.36.24.jpg"

try:
    img = cv2.imread(PIC, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError('ファイルが見つかりません')

    cv2.imshow('sample01/color', img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('sample01/gray', gray)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
