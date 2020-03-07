import calendar
import copy
import datetime
import logging.config
import os
import pickle
import sys
import time
import traceback

import mail.send_mail as gmail
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# 実行中のブラウザ表示有り無し
BROWSER_USE = True

# 次月検索フラグ(True: 次の月を検索対象, False: 現在月を検索対象)
NEXT_MONTH_SEARCH = False

# 検索するテニスコートリスト
TENNIS_COURT_LIST = r'./tennis_court_list.txt'

# 結果出力用ファイル名
OUTPUT_FILE_NAME = "search_result"
OUTPUT_FILE_EXTENSION = ".txt"

# ログ出力先
LOG_DIR_NAME = "./log"

FUREAI_URL = r"https://www.fureai-net.city.kawasaki.jp/user/view/user/homeIndex.html"

# 環境設定
# chromeドライバーのパス
CHROME_DRIVER_FULLPATH = r"./chromedriver/chromedriver.exe"

# 待機時間設定
IMPLICITLY_WAIT = 5
SLEEP = 2
LOGIN_WAIT = 5
MOVE_NEXT_PAGE_WAIT = 3
EXISTENCE_CHECK_WAIT = 1

# INDEX用文字列
ID = 1
PASSWORD = 2
TRUE_ARG_COUNT = 3
ONE_DAY_DETAILS = 1
COURT_NAME = 0
COURT_TIME = 1
COURT_BOOKING = 2

# カレンダー用設定
FIRST_DAY_OF_MONTH = 1

# 出力用ライン文字列の個数
ENCLOSING_LINE_SIZE = 20

# Windowサイズ
WINDOW_SIZE_H = 1000
WINDOW_SIZE_W = 960

# 区切り文字
# 仕様追加：区切り文字にダブルコーテーションを付ける
DELIMITER = ','
SPACE = " "

# 出力で使う日付情報
month = None
s_day = None
last_month = None

# 取得した情報を格納する辞書
output_data_dic = {}

# バックアップ用ファイル名
SAVE_FILE_NAME = './log/booking_list.pickle'

# 出力ファイル末尾の日付フォーマット
DATE_FORMAT_F_NAME = r"%Y%m%d_%H%M%S"
DATE_FORMAT_OUTPUT = r"%Y.%m.%d. %H:%M:%S"

# LINE出力用
access_token = "SutrAPnnxLH2Hpx8uA1IQd0CkNSRUMQV67XyKxEQrgd"
line_notify_url = "https://notify-api.line.me/api/notify"


def get_webdriver():
    """
    WebDriverの取得
    :return: WebDriver
    """
    if BROWSER_USE:
        # ブラウザを使う場合
        wd = webdriver.Chrome(executable_path=CHROME_DRIVER_FULLPATH)
        wd.set_window_size(WINDOW_SIZE_W, WINDOW_SIZE_H)
        wd.implicitly_wait(IMPLICITLY_WAIT)
        return wd
    else:
        if os.name == 'nt':
            # ブラウザなし(Windows)
            options = Options()
            options.add_argument('--headless')
            wd = webdriver.Chrome(chrome_options=options,
                                  executable_path=CHROME_DRIVER_FULLPATH)
            return wd
        else:
            # ブラウザなし ラズパイ(ubuntu)想定
            wd = webdriver.PhantomJS(service_log_path=os.path.devnull)
            return wd


def login(web_driver, f_id, password):
    web_driver.get(FUREAI_URL)
    web_driver.implicitly_wait(IMPLICITLY_WAIT)
    web_driver.find_element_by_id("login").click()

    # User情報入力
    # ID
    e = web_driver.find_element_by_id("userid")
    e.clear()
    e.send_keys(f_id)

    # password
    e = web_driver.find_element_by_id("passwd")
    e.clear()
    e.send_keys(password)
    time.sleep(SLEEP)

    # フォーム送信
    frm = web_driver.find_element_by_css_selector("#doLogin")
    frm.click()

    logging.info("ログインボタンを押しました。")
    time.sleep(SLEEP)


def scraping(web_driver, court_names):
    logging.debug('受け取ったリスト : {}'.format(court_names))

    # 日時情報を取得
    get_search_days()

    # 施設名毎にループ
    for court_name in court_names:
        logging.debug("URL : {}".format(web_driver.current_url))
        logging.info("検索対象の施設名 : {}".format(court_name))

        # 初期化
        output_data_dic[court_name] = []
        add_time_list = []

        # 「施設名から探す」を選択
        search_btm = web_driver.find_element_by_css_selector("#goNameSearch")
        search_btm.click()

        try:
            # 施設名を入力して、フォーム送信
            logging.info("施設名を入力して、フォーム送信します")
            logging.debug("施設名 : {}".format(court_name))
            keyword_tbox = web_driver.find_element_by_css_selector(
                'input#textKeyword')
            # web_driver.implicitly_wait(IMPLICITLY_WAIT)
            keyword_tbox.send_keys(court_name)
            web_driver.find_element_by_css_selector("input#doSearch").click()

            # 検索結果画面から施設決定(一つしか出ていない想定)
            logging.debug("URL : {}".format(web_driver.current_url))
            web_driver.find_element_by_css_selector("input#doSelect").click()
        except:
            logging.exception('施設名の検索でエラーが発生しました')

        # TODO: 次月選択
        if NEXT_MONTH_SEARCH:
            # 次月を表示させるため、処理前に次月ボタンを押す
            # 現在月がデフォルトで表示されている為、この時には前月リンクが死んでいる
            # 上記理由で最初のリンクをクリックするようにしている
            web_driver.find_element_by_css_selector('td.calender a').click()

        # 本日から月末までを確認する
        # TODO: 夕方に検索する際に本日が無くなっていないか確認
        for d in range(int(s_day), int(last_month) + 1):
            time_list = []
            day_str = str(d)
            web_driver.find_element_by_partial_link_text(day_str).click()
            # web_driver.implicitly_wait(IMPLICITLY_WAIT)

            # 情報取得
            logging.info("施設の空き情報を確認します")

            time_list.append(d)
            logging.debug(">>> 日付 : {}".format(d))
            logging.debug(">>> list : {}".format(time_list))

            # 指定日付の予約情報取得
            time_list.append(check_reservation_status(web_driver, court_name))
            logging.debug(">>> list : {}".format(time_list))

            # 日付情報をリストに加える
            add_time_list.append(copy.deepcopy(time_list))
            logging.debug('追加した情報 : {}'.format(time_list))

        # 取得した情報を施設名毎に格納
        output_data_dic[court_name] = copy.deepcopy(add_time_list)

        # 「マイページ」へ戻る(2画面前へ)
        web_driver.back()
        # web_driver.implicitly_wait(IMPLICITLY_WAIT)
        web_driver.back()
        # web_driver.implicitly_wait(IMPLICITLY_WAIT)
        logging.debug('「マイページ」へ戻りました(2画面前へ)')
        logging.debug('URL : {}'.format(web_driver.current_url))

    logging.debug("************* 取得した情報全て *************")
    logging.debug(output_data_dic)


def get_search_days():
    """
    日付情報を取得する
    検索対象が来月の場合は、検索開始日を1日にセットする。
    検索対象が今月の場合は、現在日を検索開始日としてセットする。
    :return: 月、日、月末日を返す
    """
    global month
    global s_day
    global last_month

    # 日付情報取得
    date_data = datetime.datetime.today()
    logging.debug("today : {}".format(date_data))

    if NEXT_MONTH_SEARCH:
        # 現在月を起点に考え、来月を対象とする
        dt = datetime.datetime.utcnow()

        month = date_data.month + 1
        s_day = (dt.date() - datetime.timedelta(days=dt.day - 1)).day
        last_month = calendar.monthrange(date_data.year, date_data.month + 1)[1]

    else:
        # 現在月を検索対象とする
        month = date_data.month
        s_day = date_data.day
        last_month = calendar.monthrange(date_data.year, date_data.month)[1]

    logging.debug("search_month     : {}".format(month))
    logging.debug("search_start_day : {}".format(s_day))
    logging.debug("search_end_day   : {}".format(last_month))


def check_reservation_status(web_driver, place):
    logging.debug("----------------- 予約状況取得 開始 -----------------")

    # 取得した予約情報を保持するリスト
    ret_list = []

    # 次のページが見つからない状況になるまで、無限ループ
    while True:
        logging.info("URL : {}".format(web_driver.current_url))
        # コート単位の枠 最初の値は注意書きなのでスキップしている
        booking_info_list = web_driver.find_elements_by_css_selector(
            'table.tablebg2')
        for empty_index, booking_info in enumerate(booking_info_list):

            # コート名
            try:
                court_name = "[" + place + "]" + booking_info.find_element_by_css_selector(
                    'span#inamem').text
                # court_name = booking_info.find_element_by_css_selector('span#inamem').text
            except NoSuchElementException:
                logging.debug('捕捉した情報は不要な情報(ページ間のリンク等)なのでスキップします')
                continue
            except Exception:
                logging.exception('不明なエラーが発生しました')
                logging.info('強制終了します')
                sys.exit(1)

            timezone_list = []
            timezone_names = booking_info.find_elements_by_css_selector(
                'span#tzonename')
            for i, x in enumerate(timezone_names):
                logging.debug("時間帯 {0}: {1}".format(i + 1, x.text))
                timezone_list.append(x.text)

            # 空き情報
            empty_list = []
            empty_states = booking_info.find_elements_by_css_selector(
                'img#emptyStateIcon')
            for empty_index, y in enumerate(empty_states):
                if y.get_attribute('alt') == "空き":
                    ret = '〇'
                else:
                    ret = '×'
                logging.debug("状況 {0}: {1}".format(empty_index + 1, ret))
                empty_list.append(ret)

            logging.info("コート名 : {}".format(court_name))
            logging.info(timezone_list)
            logging.info(empty_list)

            ret_list.append([court_name, timezone_list, empty_list])

        logging.debug("----------------- 予約状況取得 完了 -----------------")

        try:
            # 「次の5件」をクリック
            web_driver.find_element_by_css_selector('a#goNextPager').click()
            logging.debug('「次のページ」が見つかりました')
        except NoSuchElementException:
            # 「次の5件」が無い場合
            logging.debug('「次のページ」が見つからない為、ループから抜けます')
            logging.debug(ret_list)
            break
        except Exception:
            logging.exception('不明なエラーが発生しました')
            logging.info('強制終了します')
            sys.exit(1)

    return ret_list


def get_court_list(conf_file_path):
    with open(conf_file_path, encoding="UTF-8") as tags_file:
        tags_list = []
        for t in tags_file:
            if t[0] == "#":
                # 先頭が # の場合処理対象としない
                continue
            t = t.strip()
            tags_list.append(t)
        return tags_list


def save_temporarily_list(save_list):
    """
    シリアライズ用関数
    :param save_list: 保存するリスト
    :return: None
    """
    # シリアライズ
    with open(SAVE_FILE_NAME, mode='wb') as f:
        logging.debug("Serialize start")
        pickle.dump(save_list, f)
        logging.debug("Serialize end")


def load_temporarily_list():
    """
    デシリアライズ用関数
    :param: None
    :return: デシアライズ後のリスト
    """
    # デシアライズ
    with open(SAVE_FILE_NAME, mode='rb') as f:
        return pickle.load(f)


def output_booking_list(b_list):
    mail_send_data = []
    time_zone_list = []
    sp_line = ['-' * ENCLOSING_LINE_SIZE + "\n"]

    # コート名毎にループ
    for court_name_key in b_list.keys():
        # ループ毎に初期化
        get_time_zone = False

        logging.debug("*" * ENCLOSING_LINE_SIZE)
        logging.debug("場所 : {}".format(court_name_key))
        logging.debug("*" * ENCLOSING_LINE_SIZE)

        # 日付毎のリスト
        for list_by_date in b_list[court_name_key]:
            b_day = list_by_date[0]
            logging.debug("<< {0:02d}日 >>".format(b_day))

            # その日の全コートデータ
            one_day_details = list_by_date[ONE_DAY_DETAILS]

            for details_court in one_day_details:
                court_detail = details_court[COURT_NAME]
                booking_time = ",".join((details_court[COURT_TIME]))
                booking = ",".join((details_court[COURT_BOOKING]))

                if '〇' in details_court[COURT_BOOKING]:
                    free = True
                else:
                    free = False

                logging.debug("コート　 : {}".format(court_detail))
                logging.debug("時間帯 　: {}".format(booking_time))
                logging.debug("予約状況 : {}".format(booking))
                logging.debug("")

                # 各場所毎の時間帯取得
                if not get_time_zone:
                    # [<場所>]<コート名>　となっていて、場所だけを抜き出す
                    # court_detail                   ⇒ [<場所>]<コート名>
                    # court_detail.split(']')[0]     ⇒ [<場所>
                    # court_detail.split(']')[0][1:] ⇒ <場所>
                    p_name = court_detail.split(']')[0][1:]

                    # TODO: booking_time が、全角文字列になっているので半角に変換
                    time_zone_list.append(
                        "{} : {}\n".format(p_name, booking_time))
                    get_time_zone = True

                # メール用のデータを格納
                if free:
                    # 空きがあるものだけを対象とする
                    mail_send_data.append(
                        "{0:02d}日 | {1} | {2}\n".format(b_day, court_detail,
                                                        booking))
                    logging.debug(
                        "<<Mail送信データへ追加>>{0:02d}日 | {1} | {2}".format(b_day,
                                                                      court_detail,
                                                                      booking))

        logging.debug("■■ Mail送信データ　全体 ■■\n")
        logging.debug(mail_send_data)

    return sp_line + time_zone_list + sp_line + mail_send_data


def line_send(send_msg='no Message'):
    logging.info('LINEへ転送します')
    auth = "Bearer " + access_token
    headers = {'Authorization': auth}
    param = {'message': send_msg}

    ret = requests.post(line_notify_url, headers=headers, params=param)

    if ret.status_code != 200:
        logging.error('LINE送信に失敗しました')
        logging.error('結果コード : {}'.format(ret))


if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] == 'next':
        NEXT_MONTH_SEARCH = True

    # cron対策 実行ディレクトリ変更
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ログ出力用フォルダ
    if not os.path.isdir(LOG_DIR_NAME):
        os.makedirs(LOG_DIR_NAME, exist_ok=True)

    # logging設定
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('__name__')

    logging.debug("workフォルダ : {}".format(os.getcwd()))
    logging.debug("OS           : {}".format(os.name))

    logging.info("Start processing")
    # 引数よりIDとパスワードを受け取る
    # TODO: 時間があったらargparseを導入したい。
    # if len(sys.argv) == TRUE_ARG_COUNT:
    #     my_id = sys.argv[ID]
    #     my_password = sys.argv[PASSWORD]
    # else:
    #     logging.info("引数が不足しています。")
    #     logging.error("強制終了します")
    #     sys.exit(1)

    my_id = 1211572
    my_password = 2830

    # テキストよりタグ名を取得する
    logging.debug("Get court name from text [start]")
    t_list = get_court_list(TENNIS_COURT_LIST)
    logging.debug("Get court name from text [end]")

    wb = get_webdriver()

    login(wb, my_id, my_password)

    logging.info("Scraping start")

    # 空き情報をチェック
    scraping(wb, t_list)

    logging.info("Scraping end")

    # 取得したリストをシリアライズして保存
    logging.debug(output_data_dic)
    save_temporarily_list(output_data_dic)

    # ログアウト
    wb.find_element_by_css_selector('input#doLogout').click()
    logging.info('logged out')

    # ブラウザを閉じる
    logging.info("Close the browser")
    wb.close()

    # 結果をリストを使ってメール送信用の文字列作成
    try:
        mail_send_data_list = output_booking_list(output_data_dic)

    except Exception:
        logging.error('メール送信でエラー発生')
        logging.error(traceback.print_exc())
        logging.info('処理を終了します。')
        sys.exit(1)

    # 取得した情報をgmailとLINEへ送る
    try:
        if mail_send_data_list:
            try:
                # gmail送信
                title = "ふれあいネット検索結果 : {}月{}日 ～ {}日".format(month, s_day, last_month)
                message = "\n" + "".join(mail_send_data_list)
                gmail.send_gmail(title, message)
                logging.debug("メール送信用のデータ：{}".format(message))

            except Exception:
                logging.error('メール送信でエラー発生')
                logging.error(traceback.print_exc())
                logging.info('処理を終了します。')
                sys.exit(1)

            # LINEにて通知
            line_send("ふれあいネットの空き情報をgmailへ送信しました。")

        else:
            # LINEにて通知
            line_send("ふれあいネットの空き情報はありませんでした。")

    except Exception:
        logging.error('LINE送信でエラー発生')
        logging.error(traceback.print_exc())
        logging.info('処理を終了します。')
        sys.exit(1)

    logging.info('Processing Exit\n\n')
