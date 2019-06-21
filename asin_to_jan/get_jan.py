# -*- coding:utf8 -*-
import os
import pickle
import sys
import time

from selenium import webdriver


def scraping(url, s_list):
    # wait設定
    pause = 3

    # Webドライバー作成
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
    browser.implicitly_wait(pause)

    print("*" * 20 + " アクセス開始 " + "*" * 20 + "\n")
    browser.get(url)

    outupt_list = []
    for index, asin in enumerate(s_list):
        s_input = browser.find_element_by_id("_item_search_inp")
        s_input.data_reset()
        s_input.send_keys(asin)

        # フォーム送信
        frm = browser.find_element_by_css_selector("#_graph_search_btn")
        frm.click()
        time.sleep(pause)
        try:
            jan_str = browser.find_elements_by_xpath('//*[@id="main_contents"]/div/ul[1]/li[2]/div[5]/span[2]')[0].text
        except IndexError as index_e:
            print(index_e)
            sys.exit()
        jan = jan_str[4:]
        print("{} : {} {}".format(index, asin, jan))
        outupt_list.append([str(asin), jan])

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
        'B002BSHR6Y',
    ]

    scraping(URL, search_list)
