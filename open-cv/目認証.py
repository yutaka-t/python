# -*- coding:utf-8 -*-

import cv2
import os

# PIC = r"pic01.jpg"
# PIC = 'shinki.jpg'
# PIC = 'ski.jpg'
# PIC = 'r&s.jpg'
PIC = 'nabe.jpg'

# 目認証用のXMLファイル
XML_EYE = r"E:\Python\Python37\Lib\site-packages\cv2\data\haarcascade_eye.xml"

# 画像が大きい場合の一時保存先
TEMP_DIR = r"E:\temp"

try:
    img = cv2.imread(PIC, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError('ファイルが見つかりません')

    # 目認証のXMLファイルをセット
    cascade = cv2.CascadeClassifier(XML_EYE)
    if cascade is None:
        raise FileNotFoundError('ファイルが見つかりません')

    # 顔の検出
    eye = cascade.detectMultiScale(img)

    if len(eye) > 0:
        for r in eye:
            x, y = r[0:2]
            width, height = r[0:2] + r[2:4]

            # 検出した部分を四角で囲う
            cv2.rectangle(img, (x, y), (width, height), (255, 255, 255), thickness=2)
    else:
        print("目が見つかりません")

    # 画像データが大きい場合は表示しきれないので保存する
    # temp_file_path = os.path.join(TEMP_DIR, 'cv2.jpg')
    # cv2.imwrite(temp_file_path, img)

    # 画像表示
    cv2.imshow('sample01', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
