from flask import Flask, request, abort
import os
# Scrapeのため
#import scrape as sc
#import newsScrape as sc
#import wordSerch as ws
import sys
import json
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import urllib.request
import json
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
# import aisatsu

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
#if channel_secret is None:
#    print('Specify LINE_CHANNEL_SECRET as environment variable.')
#    sys.exit(1)
#if channel_access_token is None:
#    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#    sys.exit(1)

#line_bot_api = LineBotApi(channel_access_token)
#handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word = event.message.text
    url = "https://www.weblio.jp/content/" + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    bs = BeautifulSoup(html, 'lxml')
    try:
        meanings = bs.select_one("#cont > div:nth-child(6) > div > div.NetDicBody").text
    except AttributeError:
        meanings = "そのような言葉は見つからなかったよ...。ごめんね。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=word + '\n' + meanings.lstrip()))
""" @handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text)
#        TextSendMessage(text=event.message.text + "\nthanks"))
        # messageを変化させてみる
#        TextSendMessage(text = aisatsu.aisatsu(event.message.text))
    word = event.message.text
#    word = '船橋'
    result = ws.getWord(word)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    ) """
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
