# -*- coding:utf-8 -*-

import logging.config
import os

# ログ出力先
LOG_DIR_PATH = "./log"


def log_output_test():
    logging.debug("debug message")
    logging.info("info message")
    logging.warning("warn message")
    logging.error("error message")

    logging.info("UTF-8設定確認")
    for index, x in enumerate(range(10)):
        logging.debug('ループ中 {}'.format(index))

    dummy_list = [0, 1]
    try:
        number = 8
        msg = "loggingテスト中"

        # exceptionテスト
        print(dummy_list[100])

    except IndexError:
        logging.debug("例外テストを行います")
        e_msg = "例外テスト"
        e_info_dic = {
            "index": number,
            "e_msg": e_msg,
            "msg": msg,
        }
        logging.exception(e_info_dic)


if __name__ == '__main__':
    # 取り込み方法
    # 1. import logging.config を定義
    # 2. LOG_DIR_NAME 設定
    # 3. main の内容をコピペ
    # 4. logging.conf を同一フォルダに設置する

    # ログ設定ファイルからログ設定を読み込み
    if not os.path.isdir(LOG_DIR_PATH):
        os.makedirs(LOG_DIR_PATH, exist_ok=True)

    # 設定ファイル読み込み
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('__name__')
