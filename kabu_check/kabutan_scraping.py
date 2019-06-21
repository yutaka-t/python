# -*- coding:utf8 -*-
import os
import time

from selenium import webdriver

# ログイン情報
mail = ''
passowrd = ''

# スクリーンショット用ファイル名
# テスト用
SCREEN_SHOT_FILE_NAME_H = 'sc_shot_head.png'
SCREEN_SHOT_FILE_NAME_T = 'sc_shot_tail.png'
TEST_URL = r"http://tyn-imarket.com/stocks/search?query=6246"

LOGIN_URL = r"https://account.kabutan.jp/login"
COM_URL = r"https://kabutan.jp/stock/finance?code={}&mode=k"

# 実行中のブラウザ表示有り無し
BROWSER_USE = True

# 環境設定
# chromeドライバーのパス
CHROME_DRIVER_FULLPATH = r"./chromedriver/chromedriver.exe"

# 画面取得用設定
DISP_SPREAD_ID = "oc_b2f"
LIST_SELECTER = "div.fin_fd.fin_yfd > table > tbody > tr"
EMAIL = "session_email"
PASS = "session_password"
LOGIN = "btn-submit_blue"
IMPLICITLY_WAIT = 100
LIST_START = 1
LIST_END = -3


def scraping(finance_code):
    # wait設定
    pause = 1

    if BROWSER_USE:
        # ブラウザを使う場合
        browser = webdriver.Chrome(executable_path=CHROME_DRIVER_FULLPATH)
        browser.set_window_size(960, 960)
        browser.implicitly_wait(pause)
    else:
        # ブラウザなし
        browser = webdriver.PhantomJS(service_log_path=os.path.devnull)

    print("*" * 20 + " アクセス開始 " + "*" * 20 + "\n")

    # ログイン画面へアクセス
    browser.get(LOGIN_URL)
    browser.implicitly_wait(IMPLICITLY_WAIT)

    # ログイン情報入力 (E-MAIL)
    email_input = browser.find_element_by_id(EMAIL)
    email_input.data_reset()
    email_input.send_keys(mail)

    # ログイン情報入力 (PASSWORD)
    pass_input = browser.find_element_by_id(PASS)
    pass_input.data_reset()
    pass_input.send_keys(passowrd)
    time.sleep(pause)

    # ログイン
    login = browser.find_element_by_class_name(LOGIN)
    login.click()
    browser.implicitly_wait(pause)
    print()
    print("ログインしました。")
    print("現在のURL : {}".format(browser.current_url))

    # 情報取得
    browser.get(COM_URL.format(finance_code))
    browser.implicitly_wait(IMPLICITLY_WAIT)

    print()
    print("移動しました")
    print("現在のURL : {}".format(browser.current_url))

    # 表示幅を広げる
    expand_disp = browser.find_element_by_id(DISP_SPREAD_ID)
    expand_disp.click()
    browser.implicitly_wait(IMPLICITLY_WAIT)

    # リスト取得
    stock_infos = browser.find_elements_by_css_selector(LIST_SELECTER)

    for stock_list_index, stock_info in enumerate(stock_infos[LIST_START:LIST_END]):
        # とりあえず、取得できるか確認
        if stock_list_index < 1:
            continue
        print(stock_info.text.strip())

    # TODO : スクリーンショットお試し（のちに削除)
    # スクリーンショットテスト
    browser.get(TEST_URL)
    browser.implicitly_wait(IMPLICITLY_WAIT)
    browser.maximize_window()
    browser.find_element_by_css_selector('#tab-per').click()
    browser.implicitly_wait(IMPLICITLY_WAIT)
    browser.get_screenshot_as_file(SCREEN_SHOT_FILE_NAME_H)
    time.sleep(pause)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    browser.get_screenshot_as_file(SCREEN_SHOT_FILE_NAME_T)

    print("スクリーンショットを保存しました。")
    print(SCREEN_SHOT_FILE_NAME_H)
    print(SCREEN_SHOT_FILE_NAME_T)

    # 終了
    browser.close()


if __name__ == '__main__':
    # TODO: コードの受け取り方確認
    # TODO: 複数受け取るか、単発にするか
    f_code = '6246'

    scraping(f_code)
