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

    # 横方向のエッジ検出
    sob1 = cv2.Sobel(img, ddepth=-1, dx=0, dy=1)
    cv2.imshow('01', sob1)

    # 縦方向のエッジ検出
    sob2 = cv2.Sobel(img, ddepth=-1, dx=1, dy=0)
    cv2.imshow('02', sob2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
