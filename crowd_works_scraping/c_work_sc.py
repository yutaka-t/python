# -*- coding:utf-8 -*-
import logging.config
import os

from selenium import webdriver

# import pickle
# import sys
# import datetime
# from selenium.common.exceptions import NoSuchElementException, WebDriverException
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.keys import Keys

# Selectタグが扱えるエレメントに変化させる為の関数を呼び出す
from selenium.webdriver.support.ui import Select

# ログイン情報
LOGIN_ID = ""
LOGIN_PS = ""

# 対象URL
FIRST_URL_TO_ACCESS = "https://crowdworks.jp/public/jobs/group/development"

# 環境設定
# chromeドライバーのパス
CHROME_DRIVER_FULLPATH = r"E:/temp/chromedriver/chromedriver.exe"

# 実行中のブラウザ表示有り無し
BROWSER_USE = True

# 待機時間設定
IMPLICITLY_WAIT = 3
SLEEP = 3
LOGIN_WAIT = 60

# 出力ファイル末尾の日付フォーマット
DATE_FORMAT_F_NAME = r"%Y%m%d_%H%M%S"
DATE_FORMAT_OUTPUT = r"%Y.%m.%d. %H:%M:%S"

# logging
# ログ設定ファイルからログ設定を読み込み
LOG_DIR_NAME = "./log"
if not os.path.isdir(LOG_DIR_NAME):
    os.makedirs(LOG_DIR_NAME, exist_ok=True)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

WEB_DRIVER = ""
if BROWSER_USE:
    # ブラウザを使う場合
    WEB_DRIVER = webdriver.Chrome(executable_path=CHROME_DRIVER_FULLPATH)
    WEB_DRIVER.set_window_size(1000, 1000)
    WEB_DRIVER.implicitly_wait(IMPLICITLY_WAIT)
else:
    # ブラウザなし
    WEB_DRIVER = webdriver.PhantomJS(service_log_path=os.path.devnull)


class JobOffer(object):

    def __init__(self):
        self.target_url = ""
        self.current_url = ""
        self.next_url = ""
        self.url_list = []
        self.title_list = []

    # def print_debug_data(self, k, v):
    #     logging.debug("{} : {}".format(k, v))

    def set_target_url(self, t_url):
        self.target_url = t_url
        print_debug_data("target_url", self.target_url)

    def set_current_url(self, c_url):
        self.current_url = c_url
        print_debug_data("current_url", self.current_url)

    def set_next_url(self, n_url):
        self.next_url = n_url
        print_debug_data("next_url", self.next_url)

    def print_get_datas(self):
        for i, (l, t) in enumerate(zip(self.url_list, self.title_list)):
            print("{0:03d} | {1} {2}".format(i, l, t))


def print_debug_data(k, v):
    logging.debug("{} : {}".format(k, v))


def scraping():
    offer = JobOffer()
    offer.set_target_url(FIRST_URL_TO_ACCESS)

    WEB_DRIVER.get(FIRST_URL_TO_ACCESS)
    print("現在のURL : {}".format(WEB_DRIVER.current_url))

    #TODO: 募集終了を隠す
    # Select(WEB_DRIVER.find_element_by_xpath("//*[@id='sHour']")).select_by_value('10')
    Select(WEB_DRIVER.find_element_by_css_selector("

    while True:
        # ページのリスト取得
        for i, u in enumerate(WEB_DRIVER.find_elements_by_css_selector('div.search_results h3.item_title > a')):
            offer.url_list.append(u.get_attribute('href'))
            offer.title_list.append(u.text)

        # TODO: 次のページに移動する
        next_page_exist = False
        for page_a_tag in WEB_DRIVER.find_elements_by_css_selector("div.pagination_body a"):
            if page_a_tag.get_attribute('rel') == 'next':
                offer.set_next_url(page_a_tag.get_attribute('href'))
                WEB_DRIVER.get(offer.next_url)
                next_page_exist = True
                break

        # TODO: ループを抜ける条件を設定
        if not next_page_exist:
            break

    # 取得したリストを表示
    offer.print_get_datas()


if __name__ == '__main__':
    logging.debug('アクセス開始')

    scraping()

    # ブラウザを閉じる
    WEB_DRIVER.close()

    logging.debug('処理終了')
