#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import configparser
import tweepy
import re
import smtplib

from datetime import datetime as dt
from email.mime.text import MIMEText
from email.utils import formatdate

import time

#configuretion
config = configparser.ConfigParser()
config.read('config.ini')

CONSUMER_KEY = config.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('twitter', 'CONSUMER_SECRET')
ACCESS_TOKEN = config.get('twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('twitter', 'ACCESS_TOKEN_SECRET')

SMTP_SERVER = config.get('mail', 'SMTP_SERVER')
MAIL_ADDRESS = config.get('mail', 'MAIL_ADDRESS')
MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
MAIL_TO_ADDRESS = config.get('mail', 'MAIL_TO_ADDRESS')

def get_twitter_message(words, count):
    #twitter auth.
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # search
    list_text = []
    for word in words:
        tweets = api.search(q=word, count=count)
    for tweet in tweets:
        list_text.append(tweet.text)
#        print(tweet.text)

    list_tmp = []
    for text in list_text:
        text_tmp = text
        text_tmp = re.sub('RT .*', '', text_tmp)
        text_tmp = re.sub('@.*', '', text_tmp)
        text_tmp = re.sub('http.*', '', text_tmp)
        text_tmp = re.sub('https.*', '', text_tmp)
#        text_tmp = re.sub('#.*', '', text_tmp)
        text_tmp = re.sub('\n', '', text_tmp)
        text_tmp = text_tmp.strip()
        if text_tmp != '':
            list_tmp.append(text_tmp)

#
    list_tmp = list(set(list_tmp))
    text = '\n'.join(list_tmp)
    print(text)
    return(text)

#https://qiita.com/kawa-Kotaro/items/460977f050bf0e2828f2
def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP(SMTP_SERVER, 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(MAIL_ADDRESS, MAIL_PASSWORD)
    smtpobj.sendmail(MAIL_ADDRESS, to_addr, body_msg.as_string())
    smtpobj.close()

if __name__ == "__main__":

    for i in range(1, 500):
        words = ["#デマ"]
        count = 200
        text = get_twitter_message(words, count)

        tdatetime = dt.now()
        str_ymd = tdatetime.strftime('%Y%m%d%H%M%S')
        subject = 'キーワード　' + words[0] +' '+ str_ymd

        body_msg = create_message(MAIL_ADDRESS, MAIL_TO_ADDRESS, subject, text)
        send_mail(MAIL_ADDRESS, MAIL_TO_ADDRESS, body_msg)

        time.sleep(10800)

