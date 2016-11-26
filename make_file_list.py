#!/usr/bin/env python
# -*- coding:utf-8 -*-


def make_file_list(path, search_str):
    """
    条件指定でファイルのリストを指定
    :param path: 検索するディレクトリ
    :param search_str: 検索文字列（正規表現っぽい表現で・・）
    :return: ファイル名のリスト
    """
    import fnmatch
    import os

    f_names = []
    for f_name_tmp in os.listdir(path):
        f_name = f_name_tmp.decode('shift-jis')
        if fnmatch.fnmatch(f_name, search_str.decode('utf-8')):
            f_names.append(f_name)
        return f_names


if __name__ == '__main__':
    # 検索対象指定
    file_path = r"C\Temp"
    r_str = '*'

    # リスト取得
    ret_list = make_file_list(file_path, r_str)

    # 表示
    for x in ret_list:
        print(x)
