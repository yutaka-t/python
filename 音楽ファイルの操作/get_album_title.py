import os

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC


def number_formatting(ch):
    """
    トラック番号用の文字列を整形する
    スラッシュ(/)が入っていた場合は除去し、
    指定桁数の0字埋めした数値文字列を返却
    :param ch:トラック番号用の数値文字列
    :return:0字埋めした数値文字列
    """
    zero_num = 4
    if ch.find('/'):
        return ch.split('/')[0].zfill(zero_num)
    else:
        return ch.zfill(zero_num)


def get_album_title(music_f_path):
    """
    mp3 or flac ファイルのパスから、アルバム名とトラック番号を取得する
    :param music_f_path: mp3, flac のフルパス
    :return: アルバム名 と トラック番号 のタプル
    """
    path, ext = os.path.splitext(music_f_path)
    if ext == ".flac":
        album_title = FLAC(music_f_path)['album'][0]
        t_num_str = number_formatting(FLAC(music_f_path)['tracknumber'][0].zfill(4))
        return album_title, t_num_str

    elif ext == ".mp3":
        album_title = EasyID3(music_f_path)['album'][0]
        t_num_str = number_formatting(EasyID3(music_f_path)['tracknumber'][0])
        return album_title, t_num_str

    else:
        print("不明な拡張子を検出しました : {}".format(ext))
        print("変換処理の対象から除外します")
        print(" ⇒ {}".format(music_f_path))


if __name__ == '__main__':
    p = r"C:\Users\yutak\Desktop\test\04 Left Alone.mp3"

    print(get_album_title(p))

    p = r"C:\Users\yutak\Desktop\test\08 March On Selma.flac"

    print(get_album_title(p))
