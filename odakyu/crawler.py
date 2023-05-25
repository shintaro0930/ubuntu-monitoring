import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import csv


"""
もうすこし改良が必要
"""


"""上りを取得 平日 / 休日の順番"""
# url = "https://transfer.navitime.biz/odakyu-transit/smart/diagram/Search?startId=00004682&linkId=00000686&direction=up&nodeType=train&initDispWeekdayTab="


"""下りを取得 平日 / 休日の順番"""
url = 'https://transfer.navitime.biz/odakyu-transit/smart/diagram/Search?startId=00004682&linkId=00000686&direction=down&nodeType=train&initDispWeekdayTab=weekday'

request = requests.get(url)

soup = BeautifulSoup(request.text, 'html.parser')

# 時間情報を保持
hour_elements = soup.find_all(class_=re.compile("hour-frame"))


#with open('nobori_table_data.csv', 'a') as f:
with open('kudari_table_data.csv', 'a') as f:
    for table_data in hour_elements:
        text = table_data.text.replace('\t', '')  # タブを削除
        text = text.replace('\n', '')
        if re.match(r'\d{1,2}時', text):
            text = '\n' + text

        # テキストからパターンにマッチする部分を抽出
        result = re.findall(r'\d{1,2}時|\d{2}[\u4E00-\u9FFF]|\d{2}', text)

        # パターンにマッチした部分をコンマで結合し、最後にコンマを追加
        formatted_text = ','.join(result) + ','

        print(formatted_text)
        f.write(formatted_text)
