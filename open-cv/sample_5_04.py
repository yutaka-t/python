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

    lap1 = cv2.Laplacian(img, ddepth=-1)
    cv2.imshow('01', lap1)

    # 出力画像をfloat64とする
    lap2 = cv2.Laplacian(img, ddepth=cv2.CV_64F)
    cv2.imshow('02', lap2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
