from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time

app = Flask(__name__, static_folder='static')

train_info = {}


def get_train_color(text):
    if text == '小田急線':
        return 'odakyu-line'
    elif text == '横浜線':
        return 'yokohama-line'
    elif text == '田園都市線':
        return 'denen-line'
    elif text == '南武線':
        return 'nanbu-line'
    elif text == '学研都市線':
        return 'gakken-line'
    elif text ==  '副都心線':
        return 'hukutoshin-line'
    elif text == '千代田線':
        return 'chiyoda-line'
    else:
        return 'Error'


def get_content(text: str, url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    bool_trouble = soup.find('dd', class_='trouble')
    if bool_trouble:
        content = bool_trouble.find('p')
        if content:
            return {
                "status": f'{text}は遅延しています！',
                "content": f'{content.text}',
                "color": get_train_color(text)
            }
        else:
            return {
                "status": f'{text}は遅延しています！',
                "content": '遅延情報が見つかりませんでした',
                "color": get_train_color(text)
            }
    else:
        return {
            "status": f'{text}は通常運転です',
            "content": None,
            "color": get_train_color(text)
        }


def update_train_info():
    current_time = datetime.now().strftime("%H時%M分%S秒")
    global train_info
    train_info = {
        "current_time": current_time,
        "train_info": [
            get_content('小田急線', 'https://transit.yahoo.co.jp/diainfo/109/0'),
            get_content('横浜線', 'https://transit.yahoo.co.jp/diainfo/31/0'),
            get_content('田園都市線', 'https://transit.yahoo.co.jp/diainfo/114/0'),
            get_content('南武線', 'https://transit.yahoo.co.jp/diainfo/34/0'),
            get_content('学研都市線', 'https://transit.yahoo.co.jp/diainfo/271/0'),
            get_content('副都心線', 'https://transit.yahoo.co.jp/diainfo/540/0'),
            get_content('千代田線', 'https://transit.yahoo.co.jp/diainfo/136/0')
            # 副都心、千代田

        ]
    }


@app.route('/')
def display_train_info():
    update_train_info()
    return render_template('app.html', train_info=train_info)


if __name__ == '__main__':
    update_train_info()
    app.run(port=8000)

    while True:
        time(100)
        app.run(port=8000)
