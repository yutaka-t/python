#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import xlrd


class Excel(object):
    def __init__(self, excel_full_path):
        self.excel_path = excel_full_path
        try:
            self.book = xlrd.open_workbook(excel_full_path)

            # sheet名リスト
            self.sheet_name_list = [n.strip() for n in self.book.sheet_names()]

        except IOError as e:
            print("Excelの読み込みでエラーが発生しました")
            print(e)
            sys.exit(1)


if __name__ == '__main__':
    f_path = r"E:\temp\xxx.xls"
    my_excel = Excel(f_path)

    print(my_excel.sheet_name_list)

