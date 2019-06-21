# -*- coding:utf8 -*-
import os
import sqlite3
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# ログイン情報
mail = ''
passowrd = ''

# LOGIN_URL = r"https://account.kabutan.jp/login"
LOGIN_URL = r"https://shikiho.jp/tk/login"
COM_URL = r"https://shikiho.jp/services/Query?SRC=shikiho/basic/quarter/base&code={}"

# 実行中のブラウザ表示有り無し
BROWSER_USE = True

# 環境設定
# chromeドライバーのパス
CHROME_DRIVER_FULLPATH = r"./chromedriver/chromedriver.exe"

# 画面取得用設定(ログイン画面)
EMAIL = "i"
PASS = "p"
LOGIN = "loginButton"

# 画面取得用設定(該当企業ページ)
LIST_SELECTER = "div.gradation_box a"
BREADCRUMB_STR = ' > '
FEATURE_SELECTER = 'div.tokusyoku p'
INDEPENDENT_B_SELECTER = 'div.tokusyoku > span'
COM_PROFILE_SELECTER = 'div#profile'
ARTICLE_SELECTER = 'div.kiji tr'
SHAREHOLDER_INFO_SELECTER = 'div.kabunushi'
SHAREHOLDER_DETAILS = '▶株主の詳細を見る'
EXECUTIVE_DETAILS = '▶役員の詳細を見る'
LIST_START = 0
LIST_END = 7

# 待機時間設定
IMPLICITLY_WAIT = 3
SLEEP = 1


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


def login(web_driver):
    """
    Kabutan へログインを行う
    :param web_driver: WebDriver
    :return: None
    """
    # ログイン画面へアクセス
    web_driver.get(LOGIN_URL)
    web_driver.implicitly_wait(IMPLICITLY_WAIT)

    # ログイン情報入力 (E-MAIL)
    email_input = web_driver.find_element_by_id(EMAIL)
    email_input.data_reset()
    email_input.send_keys(mail)

    # ログイン情報入力 (PASSWORD)
    pass_input = web_driver.find_element_by_id(PASS)
    pass_input.data_reset()
    pass_input.send_keys(passowrd)
    time.sleep(SLEEP)

    # ログイン
    login_button = web_driver.find_element_by_id(LOGIN)
    login_button.click()
    web_driver.implicitly_wait(IMPLICITLY_WAIT)


def weblist2str(l, join_str=None):
    tmps = [x.text for x in l]
    if join_str:
        ret = join_str.join(tmps)
    else:
        ret = "".join(tmps)
    return ret


def scraping(finance_code):
    # webdriver取得
    browser = get_webdriver()

    # ログイン
    login(browser)

    # 対象画面の表示
    browser.get(COM_URL.format(finance_code))
    browser.implicitly_wait(IMPLICITLY_WAIT)

    DATA_DISP_INDEX = 0
    CHART_SELECTER = 'div#chartBody > div'
    NEWS_BODY_SELECTER = 'div#newsBody > div'
    NEWS_DETAIL_SELECTER = 'div.chartNewsDetail tbody > tr'

    try:
        # チャート
        chart_datas = browser.find_elements_by_css_selector(CHART_SELECTER)
        for index, c_data in enumerate(chart_datas):
            if index == 0:
                # データ表示領域
                continue
            else:
                c_data.click()
                browser.implicitly_wait(IMPLICITLY_WAIT)
                # 表示テスト
                print(chart_datas[DATA_DISP_INDEX].text)

        time.sleep(SLEEP)
        # ニュース概要
        news = []
        news_body = browser.find_elements_by_css_selector(NEWS_BODY_SELECTER)
        for index, nb in enumerate(news_body):
            nb.click()
            # TODO: 待ち時間はマシン性能にもよる。画面側のレスポンスが遅れて取得できないケースがある
            time.sleep(1)
            browser.implicitly_wait(IMPLICITLY_WAIT)
            # 表示テスト
            for x in browser.find_elements_by_css_selector(NEWS_DETAIL_SELECTER):
                disp = x.text.strip()
                if disp:
                    print(disp)
                    news.append(disp.replace(" ", ",", 2).split(","))

    except NoSuchElementException as nosuch_e:
        print("===================================")
        print("type : {}".format(type(nosuch_e)))
        print("args : {}".format(nosuch_e.args))
        print(nosuch_e)
        sys.exit(1)

    except Exception as e:
        print("===================================")
        print("type : {}".format(type(e)))
        print("args : {}".format(e.args))
        print(e)
        sys.exit(1)

    # ブラウザを閉じる
    browser.close()

    # SQLlist お試し
    con = sqlite3.connect(":memory:")

    # テーブル定義
    table = """
        create table chartNewsDetail (
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            detail TEXT NOT NULL
        )
    """

    # テーブル作成
    con.execute(table)

    # SQL文
    sql = r"insert into chartNewsDetail values(?, ?, ?)"

    # データ投入
    for n in news:
        con.execute(sql, n)

    # データ取得(全出力)
    c = con.cursor()
    c.execute(u"select * from chartNewsDetail")
    print("\n" + "*" * 50 + "<<全出力>>\n")
    for row in c:
        print(row)

    # データ取得(概要のみ)
    c2 = con.cursor()
    c2.execute(u"select detail from chartNewsDetail")
    print("\n" + "*" * 50 + "<<概要のみ出力>>\n")
    for row in c2:
        print(row)

    # DBを閉じる
    con.close()


if __name__ == '__main__':
    # TODO: コードの受け取り方確認
    # TODO: 複数受け取るか、単発にするか
    f_code = '6246'

    scraping(f_code)
