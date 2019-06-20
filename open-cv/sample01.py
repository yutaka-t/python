# coding:utf-8
import cv2

PIC = r"C:\Users\yutak\Dropbox\Camera Uploads\2019-03-16 12.50.39-1.jpg"
PIC2 = r"C:\Users\yutak\Dropbox\Camera Uploads\2018-10-27 15.36.24.jpg"

try:
    img1 = cv2.imread(PIC2, cv2.IMREAD_GRAYSCALE)
    if img1 is None:
        raise FileNotFoundError("①ファイルが見つかりません")

    # カラー画像で読み込む
    img2 = cv2.imread(PIC, cv2.IMREAD_COLOR)
    if img2 is None:
        raise FileNotFoundError("ファイルが見つかりません")

    # cv2.imshow('sample01', img1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print("img1 : {}".format(img1.shape))
    print("img2 : {}".format(img2.shape))

    print(img2[2500][1000][0])

except FileNotFoundError as e:
    print(e)
