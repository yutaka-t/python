# -*- coding:utf8 -*-
import os
import sqlite3
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


d = [
    '17/03/24 16:00 東証TDnet 配当予想の修正に関するお知らせ (PDF)',
    '17/03/24 16:00 株探ニュース Ｔスマート、今期配当を6円増額修正',
    '17/03/24 17:06 株探ニュース ★本日の【サプライズ決算】 速報　（3月24日）',
    '17/04/14 11:50 東証TDnet 公認会計士等の異動に関するお知らせ (PDF)',
    '17/05/12 16:00 東証TDnet 平成29年3月期決算短信〔日本基準〕（非連結）(要約) (PDF)',
    '17/05/12 16:00 東証TDnet 平成29年3月期決算短信〔日本基準〕（非連結） (PDF)',
    '17/05/12 16:00 東証TDnet 役員の異動に関するお知らせ (PDF)',
    '17/05/12 16:00 東証TDnet 剰余金の配当に関するお知らせ (PDF)',
    '17/05/12 16:00 東証TDnet 平成29年3月期通期業績予想との差異に関するお知らせ (PDF)',
    '17/05/12 16:00 株探ニュース Ｔスマート、前期経常が上振れ着地・今期は16％増益へ',
    '17/06/08 08:00 東証TDnet 第83期定時株主総会招集ご通知 (PDF)',
    '17/06/26 17:00 ランキング ｢四季報先取り超サプライズ｣上昇率ランキング',
    '17/06/27 15:08 東証TDnet コーポレート・ガバナンスに関する報告書 2017/06/28 (PDF)',
    '17/06/27 16:00 東証TDnet 取締役の異動に関するお知らせ (PDF)',
    '17/07/21 13:50 大量保有速報 大和証券投資信託委託　テクノスマート（6246）株に係る大量保有報告書を提出',
]

news = []
for x in d:
    news.append(x.replace(" ", ",", 2).split(","))


# SQLlist お試し
con = sqlite3.connect(":memory:")

# テーブル定義
table = """
    create table chartNewsDetail (
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        detail TEXT NOT NULL
    );
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
print("*" * 50 + "<<全出力>>")
for row in c:
    print(row)

# データ取得(概要のみ)
c2 = con.cursor()
c2.execute(u"select detail from chartNewsDetail")
print("\n" + "*" * 50 + "<<概要のみ出力>>")
for row in c2:
    print(row)


# DBを閉じる
con.close()
