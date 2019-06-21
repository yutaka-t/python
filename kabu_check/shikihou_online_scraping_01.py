# -*- coding:utf8 -*-
import os
import time

from selenium import webdriver

# ログイン情報
mail = ''
passowrd = ''

# LOGIN_URL = r"https://account.kabutan.jp/login"
LOGIN_URL = r"https://shikiho.jp/tk/login"
COM_URL = r"https://shikiho.jp/tk/stock/info/{}"

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

    # パンくずリスト
    breadcrumbs = weblist2str(browser.find_elements_by_css_selector(LIST_SELECTER), BREADCRUMB_STR)
    print(breadcrumbs)

    # 特色
    feature = browser.find_element_by_css_selector(FEATURE_SELECTER).text

    # 単独事業
    independent_b = weblist2str(browser.find_elements_by_css_selector(INDEPENDENT_B_SELECTER))

    # 会社プロフェール
    com_profile = browser.find_element_by_css_selector(COM_PROFILE_SELECTER).text

    # 記事　※増減が予想されるのでリストで取得
    # TODO: 無い場合があるか?
    articles = [x.text for x in browser.find_elements_by_css_selector(ARTICLE_SELECTER)]

    # 株主情報
    shareholder_infos = [x.text for x in browser.find_elements_by_css_selector(SHAREHOLDER_INFO_SELECTER)]
    shareholder_infos = \
        [x for x in shareholder_infos[0].split('\n') if x != SHAREHOLDER_DETAILS and x != EXECUTIVE_DETAILS]

    print(feature)
    print(independent_b)
    print(com_profile)
    for article in articles:
        print(article)
    for shareholder_info in shareholder_infos:
        print(shareholder_info)

    # 終了
    browser.close()


if __name__ == '__main__':
    # TODO: コードの受け取り方確認
    # TODO: 複数受け取るか、単発にするか
    f_code = '6246'

    scraping(f_code)
