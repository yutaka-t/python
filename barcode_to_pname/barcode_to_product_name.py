# -*- coding:utf-8 -*-

import urllib.request as req

from bs4 import BeautifulSoup

# 個人で取得したAPIのコード
YAHOO_API_CODE = r""

# APIを使ってバーコードから商品名を取得するように引数をセット
URL = r"http://shopping.yahooapis.jp/ShoppingWebService/V1/itemSearch?appid={0}&jan={1}"


def barcode_to_product_info(barcode_product):
    print('*********** start product_info ************')

    product_info = "見つかりませんでした。"
    url = URL.format(YAHOO_API_CODE, barcode_product)

    res = req.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    res = soup.find('name')

    if res and len(res) > 0:
        product_info = res.string

    print(product_info)
    print('*********** end product_info ************')


if __name__ == '__main__':
    print("<バーコード(JANコード)番号を入力してください>")

    # barcode_to_product_info('4910038090484')
    barcode_to_product_info(input())
