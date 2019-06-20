import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formatdate

FROM_ADDRESS = ''
TO_ADDRESS = ''
BCC = ''
SUBJECT = 'mail送信テスト2'
BODY = 'pythonでメール送信'

MAIL_PASSWORD_INDEX = 1


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, mail_app_pass, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, mail_app_pass)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':
    # 引数でパスワード受け取り(gmailのアプリ用パスワード)
    app_pass = sys.argv[MAIL_PASSWORD_INDEX]

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = BODY

    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    send(FROM_ADDRESS, to_addr, app_pass, msg)
