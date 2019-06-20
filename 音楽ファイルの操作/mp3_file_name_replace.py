# -*- coding:utf-8 -*-
#############################################################
# Media Go で、mp3に変換したファイルに対し、
# アルバム名をファイル名に変換して連番を付ける
# ※家のコンポで再生する際にこれで変換する
#############################################################
import logging.config
import os
import os.path
import shutil
import sys

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC

# ログ出力先
LOG_DIR_PATH = "./log"

# ログ設定ファイルからログ設定を読み込み
if not os.path.isdir(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH, exist_ok=True)

# 設定ファイル読み込み
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('__name__')

# 付与するファイル名(引数受け取り)
FILE_NAME_APPEND = ""

# バックアップ用フォルダ名(バックアップは直近実行の保存)
BK_DIR_NAME = "bak"

# リネーム後の音楽ファイルに付与するトラック番号の桁数
# 桁数に満たない場合は0で埋める
ZERO_FILL_NUM = 4

TARGET_INDEX = 0

# ファイル名で使えない文字列
not_unusable_st_dic = {
    ':': '',
    '\\': '',
    '/': '',
    '*': '',
    '?': '',
    '"': '',
    '[': '',
    ']': '',
    '|': '',
}


def number_formatting(ch):
    """
    トラック番号用の文字列を整形する
    スラッシュ(/)が入っていた場合は除去し、
    指定桁数の0字埋めした数値文字列を返却
    :param ch:トラック番号用の数値文字列
    :return:0字埋めした数値文字列
    """
    if ch.find('/'):
        return ch.split('/')[TARGET_INDEX].zfill(ZERO_FILL_NUM)
    else:
        return ch.zfill(ZERO_FILL_NUM)


def get_album_title(music_f_path):
    """
    mp3 or flac ファイルのパスから、アルバム名とトラック番号を取得する
    :param music_f_path: mp3, flac のフルパス
    :return: アルバム名,トラック番号,ファイル形式のタプル
    """
    path, ext = os.path.splitext(music_f_path)
    if ext == ".flac":
        album_title = FLAC(music_f_path)['album'][TARGET_INDEX]
        t_num_str = number_formatting(FLAC(music_f_path)['tracknumber'][TARGET_INDEX].zfill(4))
        return album_title, t_num_str, ext

    elif ext == ".mp3":
        album_title = EasyID3(music_f_path)['album'][TARGET_INDEX]
        t_num_str = number_formatting(EasyID3(music_f_path)['tracknumber'][TARGET_INDEX])
        return album_title, t_num_str, ext

    else:
        logging.info("不明な拡張子を検出しました : {}".format(ext))
        logging.info("変換処理の対象から除外します")
        logging.info(" ⇒ {}".format(music_f_path))


def make_bk_dir():
    """
    対象ファイルバックアップ
    :return: None
    """
    bk_dir = os.path.join(FILE_DIR, BK_DIR_NAME)
    # バックアップフォルダが既にあったら消す
    if os.path.isdir(bk_dir):
        shutil.rmtree(bk_dir)
    shutil.copytree(FILE_DIR, bk_dir)


def file_rename():
    """
    ファイル内の情報を抽出してリネームする。
    複数のアルバムが入ったフォルダを対象とするケースがある為、
    ファイル名の先頭は、アルバム名とする。

    ※これはコンポの仕様に合わせる為にリネームしている。
    ※ノンストップのアルバムがあるので、曲の順番を変えないようにすること
    ※【注】ファイル名に空白があるとコンポが認識しない

    例) アルバム名 aName, トラック番号 8 だった場合
     　01_xxx.mp3 ⇒ aName_0008.mp3

    例) 文字列 tano を引数指定で、アルバム名 aName, トラック番号 8 だった場合
        01_xxx.mp3 ⇒ aName_0008_tano.mp3

    :return: None
    """
    # for file_name in os.listdir(FILE_DIR):
    for index, file_name in enumerate(os.listdir(FILE_DIR)):
        before = os.path.join(FILE_DIR, file_name)
        # ファイルのみを処理対象とする
        if os.path.isfile(before):

            # 音楽ファイルから、ファイル名の基になる情報を抽出
            album_name, tracknumber, ext = get_album_title(before)

            # アルバム名からスペースを代替え文字に変換
            album_name = album_name.replace(' ', '_') + '_'
            album_name = convert_unusable_characters(album_name)

            # リネーム
            after = os.path.join(FILE_DIR, album_name + tracknumber + FILE_NAME_APPEND + ext)

            try:
                os.rename(before, after)
            except FileExistsError as err:
                logging.info("重複ファイルなので除去します : {}".format(before))
                os.remove(before)

            logging.info("{} ⇒ {}".format(before, after))


def convert_unusable_characters(chk_str):
    """
    ファイル名で使えない文字列を除去する
    :param chk_str: 確認したい文字列
    :return: 除去された文字列
    """
    for key, value in not_unusable_st_dic.items():
        chk_str = chk_str.replace(key, value)

    return chk_str


if __name__ == '__main__':
    if len(sys.argv) == 3:
        FILE_NAME_APPEND = "_" + sys.argv[2]
    elif len(sys.argv) == 2:
        FILE_NAME_APPEND = ""
    else:
        logging.info("引数を確認してください。")
        logging.info("argv 1 [リネームする音楽ファイルがあるフォルダ]")
        logging.info("argv 2 [(Option)リネーム時に付与する文字列    ]")
        sys.exit(0)

    # 置換対象ファイルのある場所(引数受け取り)
    FILE_DIR = sys.argv[1]

    # バックアップディレクトリ作成
    make_bk_dir()

    # ファイルリネーム
    file_rename()
