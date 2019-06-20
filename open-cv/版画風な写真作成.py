# -*- coding:utf-8 -*-

import cv2

import numpy as np

# PIC = r"pic01.jpg"
# PIC = r"C:\Users\yutak\Dropbox\Camera Uploads\2018-10-27 15.36.24.jpg"
# PIC = 'shinki.jpg'
# PIC = 'ski.jpg'
# PIC = 'nabe.jpg'
PIC = 'r&s.jpg'

try:
    img = cv2.imread(PIC, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError('ファイルが見つかりません')

    # ret, dst = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow('sample02', dst)

    # 近傍の平均からCを引いた値をしきい値とする
    ada1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('sample01', ada1)

    # 近傍の重み付け平均値からCを引いた値をしきい値とする
    ada2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('sample02', ada2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
