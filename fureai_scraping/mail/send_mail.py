#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


FROM_ADDRESS = ''
TO_ADDRESS = ''
MAIL_PASSWORD = ''

BCC = ''
SUBJECT = 'mail送信テスト2'
BODY = 'pythonでメール送信'


def _create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def _send(from_addr, to_addrs, mail_app_pass, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, mail_app_pass)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


def send_gmail(subject=SUBJECT, body=BODY):
    app_pass = MAIL_PASSWORD
    to_addr = TO_ADDRESS

    msg = _create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    _send(FROM_ADDRESS, to_addr, app_pass, msg)


if __name__ == '__main__':
    send_gmail()
