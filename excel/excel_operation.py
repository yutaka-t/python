#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

import xlrd


class Excel(object):
    def __init__(self, excel_full_path):
        self.full_path = excel_full_path
        self.file_name = os.path.basename(self.full_path)
        self.current_dir = os.path.abspath(os.path.dirname(self.full_path))
        self.all_sheet_obj = {}
        try:
            self.book = xlrd.open_workbook(excel_full_path)

        except IOError as e:
            print("Excelの読み込みでエラーが発生しました")
            print(e)
            sys.exit(1)

        # sheet名リスト
        self.sheet_name_list = [n.strip() for n in self.book.sheet_names()]

        for s_index in range(len(self.sheet_name_list)):
            # シート毎のオブジェクト辞書 {シート名：オブジェクト}
            self.all_sheet_obj[self.book.sheet_by_index(s_index).name] = self.book.sheet_by_index(s_index)

    def get_sheet_obj_by_sheet_name(self, sheet_name):
        """
        シートのオブジェクトを返す
        :param sheet_name: シート名
        :return: シートのオブジェクト
        """
        return self.all_sheet_obj[sheet_name]

    def get_specified_row(self, sheet_name, col):
        """
        指定列のデータを全て取得する
        :param sheet_name: シート名
        :param col: 取得列(アルファベット or 数値)
        :return: 取得文字列のリスト
        """
        ret_list = []
        if type(col) is str:
            col = char2num(col.upper())

        so = self.all_sheet_obj[sheet_name]
        if so.ncols >= col:
            for r_index in range(so.nrows):
                ret_list.append(so.cell(r_index, col).value)
        return ret_list

    def get_specified_col(self, sheet_name, row):
        """
        指定列のデータを全て取得する
        :param sheet_name: シート名
        :param row: 取得列（アルファベット or 数値)
        :return: 取得文字列のリスト
        """
        # TODO: 作成中
        None


def num2char(num):
    """
    数字をアルファベットに変換 1 -> A , 27 -> AA
    :param num: Excel列用のアルファベットに対応する数値
    :return: Excel列用のアルファベット
    """
    quotient, remainder = divmod(num, 26)
    chars = ''
    if quotient > 0:
        chars = chr(quotient + 64)
    if remainder > 0:
        chars += chr(remainder + 64)
    return chars


def char2num(chars):
    """
    Excel列用のアルファベットを数字に変換 A -> 1 , AA -> 27
    :param chars: Excel列用のアルファベット
    :return: Excel列用のアルファベットに対する数値
    """
    num = 0
    for c in chars:
        num = num * 26 + (ord(c) - 64)
    return num


if __name__ == '__main__':
    f_path = r"E:\temp\xxx.xls"
    my_excel = Excel(f_path)

    print(my_excel.sheet_name_list)
