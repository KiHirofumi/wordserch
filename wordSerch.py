from bs4 import BeautifulSoup
import urllib.request
import json
import requests

#@handler.add(MessageEvent, message=TextMessage)
def getWord(word):
#def handle_message(event):
#    Word = event.message.text
    url = "https://www.weblio.jp/content/" + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    bs = BeautifulSoup(html, 'lxml')
    try:
        meanings = bs.select_one("#cont > div:nth-child(6) > div > div.NetDicBody").text
    except AttributeError:
        meanings = "そのような言葉は見つからなかったよ...。ごめんね。"
    return(meanings)

#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=word + '\n' + meanings.lstrip()))