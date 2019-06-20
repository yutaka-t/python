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

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Shi-Tomasi のコーナー検出
    corners1 = cv2.goodFeaturesToTrack(gray, 100, 0.01, 20.0, blockSize=3, useHarrisDetector=False)
    img1 = img
    for i in corners1:
        x, y = i.ravel()
        cv2.circle(img1, (x, y), 4, (255, 255, 255), -1)
    cv2.imshow('sample01', img1)

    # Harris のコーナー検出
    corners2 = cv2.goodFeaturesToTrack(gray, 100, 0.01, 20.0, blockSize=3, useHarrisDetector=True)
    img2 = img
    for i in corners2:
        x, y = i.ravel()
        cv2.circle(img1, (x, y), 4, (255, 255, 255), -1)
    cv2.imshow('sample02', img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
