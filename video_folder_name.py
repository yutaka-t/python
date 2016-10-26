#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import re

V_DIR = r"E:\Video"
V_TEMP_DIR = r"E:\Video\temp"


def dir_chk():
    """
    ディレクトリチェック
    :return:
    """
    return os.path.isdir(V_TEMP_DIR)


def err_msg_print(msg="ERROR", msg2="tmp"):
    """
    エラーメッセージ用関数
    :param msg: メッセージの内容
    :param msg2: チェックしたディレクトリパス
    :return: None
    """
    print(msg)
    if msg2 == "tmp":
        print(" --> チェックしたフォルダ : {0}".format(V_TEMP_DIR))
    else:
        print(" --> チェックしたフォルダ : {0}".format(dir))
    sys.exit(1)


def get_file_list(target_dir):
    """
    指定ディレクトリ内のファイルリストを取得する
    :param target_dir: 対象とするディレクトリ
    :return: ファイル名のリスト
    """
    f_list = os.listdir(target_dir)
    if len(f_list) == 0:
        err_msg_print("ディレクトリの中にファイルがありません。")

    else:
        f_list.sort()
        return f_list


def edit_date_str(date_str):
    ret_date_str = date_str.replace("cap-", "").replace("_", "")
    ret_date_str = re.sub("-.+$", "", ret_date_str)

    return ret_date_str


def make_dir(new_dir_full_path):
    if os.path.isdir(new_dir_full_path):
        err_msg_print("作成予定のディレクトリが存在します。", "dir")
    else:
        # test
        pass


if __name__ == '__main__':
    if dir_chk():
        files = get_file_list(V_TEMP_DIR)
        day_from = edit_date_str(files[0])
        day_to = edit_date_str(files[-1])
        # print("{0} ～ {1}".format(day_from, day_to))
        new_dir_name = day_from + "-" + day_to

        make_dir(os.path.join(V_DIR, new_dir_name))
    else:
        err_msg_print("ディレクトリが存在しません。")
