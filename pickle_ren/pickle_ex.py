import logging.config
import pickle

URL_TEMP_FILE = 'url.pickle'
MSG_TEMP_FILE = 'msg.pickle'


def save_temporarily_list(save_list, list_type='URL'):
    """
    シリアライズ用関数
    :param save_list: 保存するリスト
    :param list_type: 作成するpickleファイル名を決定付けるキーワード
    :return: None
    """
    if list_type == 'URL':
        save_file_name = URL_TEMP_FILE
    else:
        save_file_name = MSG_TEMP_FILE

    # シリアライズ
    with open(save_file_name, mode='wb') as f:
        logging.debug("シリアライズ開始 list_type = {}".format(list_type))
        pickle.dump(save_list, f)
        logging.debug("シリアライズ終了")


def load_temporarily_list(list_type='URL'):
    """
    デシリアライズ用関数
    :param list_type: デシアライズ対象となるpickleファイル名を決定付けるキーワード
    :return: デシアライズ後のリスト
    """
    if list_type == 'URL':
        pickle_file_name = URL_TEMP_FILE
    else:
        pickle_file_name = MSG_TEMP_FILE

    # デシアライズ
    with open(pickle_file_name, mode='rb') as f:
        logging.debug("デシリアライズ実行 list_type = {} : ※完了メッセージ出力なし".format(list_type))
        return pickle.load(f)


class PTest:
    def __init__(self):
        self.x = 1

    def loop_test(self):
        for x in range(self.x, 100):
            self.x = x
            print(x)

            if x % 10 == 0:
                self.x = x + 1
                print("break : x = {}".format(x))
                break


if __name__ == '__main__':
    p = PTest()

    p.loop_test()
    p.loop_test()

    # シリアライズで状態を保持
    save_file_name = 'test.pickle'
    with open(save_file_name, mode='wb') as f:
        pickle.dump(p, f)

    # デシアライズして、状態を復元できることを確認
    with open(save_file_name, mode='rb') as f:
        p2 = pickle.load(f)

    p2.loop_test()
