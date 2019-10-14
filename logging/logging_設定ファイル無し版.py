# -*- coding:utf-8 -*-
import logging

# level: 指定レベル以上を出力
# filename: 出力先ファイル
# asctime: 実行時間
# lineno: メッセージ出力箇所(行番号)
# message: メッセージ
# name: __name__ の内容が入る
#
# ◆ロギング
# https://docs.python.org/ja/3/library/logging.html
#
# ◆ハンドラ
# https://docs.python.org/ja/3/library/logging.handlers.html


# logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(filename='test.log', level=logging.WARNING)

formatter = '%(asctime)s %(levelname)s: %(lineno)d: %(message)s'
logging.basicConfig(level=logging.WARNING, format=formatter)

logging.critical('critical')
logging.error('error')
logging.warning('warning')
logging.info('info')
# 上でWARNING以上と設定している為、出力されない
logging.debug('debug')

# ----------------------------------------------------------------------------

# ロガー作成
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ハンドラ作成
h = logging.FileHandler('xxx.log')

# フォーマッター作成
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
# フォーマッターをハンドラにセット
h.setFormatter(formatter)

# ハンドラとフォーマッタをロガーに登録
logger.addHandler(h)

# 設定変更したので出力される(但し、出力先はファイルになる)
logger.debug('debug')

