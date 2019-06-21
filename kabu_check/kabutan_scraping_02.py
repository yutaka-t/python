# -*- coding:utf8 -*-
import os
import time

from selenium import webdriver

# ログイン情報
mail = ''
passowrd = ''

LOGIN_URL = r"https://account.kabutan.jp/login"
COM_URL = r"https://kabutan.jp/stock/news?code={}"

# 実行中のブラウザ表示有り無し
BROWSER_USE = True

# 環境設定
# chromeドライバーのパス
CHROME_DRIVER_FULLPATH = r"./chromedriver/chromedriver.exe"

# 画面取得用設定(ログイン画面)
EMAIL = "session_email"
PASS = "session_password"
LOGIN = "btn-submit_blue"

# 画面取得用設定(該当企業ページ)
LIST_SELECTER = "div#news_contents tr"
LIST_START = 0
LIST_END = 7

# 待機時間設定
IMPLICITLY_WAIT = 3
SLEEP = 3


def get_webdriver():
    """
    WebDriverの取得
    :return: WebDriver
    """
    if BROWSER_USE:
        # ブラウザを使う場合
        browser = webdriver.Chrome(executable_path=CHROME_DRIVER_FULLPATH)
        browser.set_window_size(960, 960)
        browser.implicitly_wait(IMPLICITLY_WAIT)
    else:
        # ブラウザなし
        browser = webdriver.PhantomJS(service_log_path=os.path.devnull)

    return browser


def login(br_obj):
    """
    Kabutan へログインを行う
    :param br_obj: WebDriver
    :return: None
    """
    # ログイン画面へアクセス
    br_obj.get(LOGIN_URL)
    br_obj.implicitly_wait(IMPLICITLY_WAIT)

    # ログイン情報入力 (E-MAIL)
    email_input = br_obj.find_element_by_id(EMAIL)
    email_input.data_reset()
    email_input.send_keys(mail)

    # ログイン情報入力 (PASSWORD)
    pass_input = br_obj.find_element_by_id(PASS)
    pass_input.data_reset()
    pass_input.send_keys(passowrd)
    time.sleep(SLEEP)

    # ログイン
    login_button = br_obj.find_element_by_class_name(LOGIN)
    login_button.click()
    br_obj.implicitly_wait(IMPLICITLY_WAIT)


def scraping(finance_code):
    # webdriver取得
    browser = get_webdriver()

    # ログイン
    login(browser)

    # 対象画面の表示
    browser.get(COM_URL.format(finance_code))
    browser.implicitly_wait(IMPLICITLY_WAIT)

    # リスト取得
    stock_infos = browser.find_elements_by_css_selector(LIST_SELECTER)

    for stock_list_index, stock_news in enumerate(stock_infos[LIST_START:LIST_END]):
        # TODO: 出力フォーマットの認識合わせ
        stock_news_url = stock_news.find_element_by_css_selector('a').get_attribute('href').strip()
        print("{0:02d} : {1} {2}".format(stock_list_index + 1, stock_news.text.strip(), stock_news_url))

    # 終了
    browser.close()


if __name__ == '__main__':
    # TODO: コードの受け取り方確認
    # TODO: 複数受け取るか、単発にするか
    f_code = '6246'

    scraping(f_code)
