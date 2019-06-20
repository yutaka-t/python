# -*- coding:utf-8 -*-

import requests
import json

# 参考：https://notify-bot.line.me/doc/ja/
access_token = ""
line_notify_url = "https://notify-api.line.me/api/notify"


def send_message():
    message = "送信テスト"

    auth = "Bearer " + access_token
    content_type = 'multipart/form-data'

    # headers = {'Method': 'POST', 'Content-Type': content_type, 'Authorization': auth}
    # headers = {'Method': 'POST', 'Content-Type': content_type, 'Authorization': auth}
    headers = {'Authorization': auth}
    param = {'message': message}

    # imageFileは、filesキーワードで送信する
    #files = {"imageFile": open("test.jpg", "rb")}

    ret = requests.post(line_notify_url, headers=headers, params=param)

    print(ret)


if __name__ == '__main__':
    send_message()
