# -*- coding:utf8 -*-
import os
import pickle
import time

from selenium import webdriver


def scraping(url, s_list):
    # wait設定
    pause = 1

    # Webドライバー作成
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
    browser.implicitly_wait(pause)

    print("*" * 20 + " アクセス開始 " + "*" * 20 + "\n")
    browser.get(url)

    outupt_list = []
    for index, search_id in enumerate(s_list):
        s_input = browser.find_element_by_id("_item_search_inp")
        s_input.data_reset()
        s_input.send_keys(search_id)

        # フォーム送信
        frm = browser.find_element_by_css_selector("#_graph_search_btn")
        frm.click()
        time.sleep(pause)

        asin = browser.find_element_by_css_selector(r'#_asin').text
        print("{} : {} {}".format(index, search_id, asin))
        outupt_list.append([str(search_id), asin])

    # 終了
    browser.close()

    # 念のため、シリアライズ
    with open('get_asin.pickle', mode='wb') as f:
        pickle.dump(outupt_list, f)

    # デシアライズ
    # with open('get_asin.pickle', mode='rb') as f:
    #     load_data = pickle.load(f)
    #     print(load_data)

    # 結果表示
    print("\n" + "*" * 20 + " 結果表示 " + "*" * 20 + "\n")
    for ret in outupt_list:
        print("\t".join(ret))


if __name__ == '__main__':
    URL = r"https://mnrate.com/"

    search_list = [
        4938833009746,
        4562226430352,
        4938833009999
    ]

    scraping(URL, search_list)
