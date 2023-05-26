from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
import re


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
    current_time = datetime.now().strftime("%H時%M分")
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
        ]
    }

def get_nobori_nearest_times(csv_file):
    now = datetime.now() 
    current_date = datetime.now().date()   
    kanji_pattern = re.compile(r'[\u4E00-\u9FFF]')
    
    times = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                hour = row[0].replace('時', '')
                for minute in row[1:]:
                    time_str = hour + ':' + minute
                    kanji_match = kanji_pattern.search(time_str)
                    if kanji_match:
                        kanji = kanji_match.group()
                        time_str = kanji_pattern.sub('', time_str)
                        if kanji == '我':
                            destination = '我孫子'
                        elif kanji == '綾':
                            destination = '綾瀬'
                        elif kanji == '経':
                            destination = '経堂'
                        elif kanji == '成':
                            destination = '成城学園前'
                        elif kanji == '向':
                            destination = '向ヶ丘遊園'
                        elif kanji == '松':
                            destination = '松戸'
                    else:
                        destination = '新宿'
                    try:
                        time = datetime.strptime(time_str, '%H:%M')
                        time = time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                        times.append((time, destination))
                    except ValueError as e:
                        pass
                    time_str = ''
    
    nearest_times = []
    for time, destination in times:
        if time >= now:
            nearest_times.append((time, destination))
        if len(nearest_times) == 3:
            break
    
    return nearest_times

def get_kudari_nearest_times(csv_file):
    now = datetime.now()
    current_date = datetime.now().date()
    kanji_pattern = re.compile(r'[\u4E00-\u9FFF]')
    
    times = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                hour = row[0].replace('時', '')
                for minute in row[1:]:
                    time_str = hour + ':' + minute
                    kanji_match = kanji_pattern.search(time_str)
                    if kanji_match:
                        kanji = kanji_match.group()
                        time_str = kanji_pattern.sub('', time_str)
                        if kanji == '百':
                            destination = '新百合ヶ丘'
                        elif kanji == '伊':
                            destination = '伊勢原'
                        elif kanji == '唐':
                            destination = '唐木田'
                        elif kanji == '大':
                            destination = '相模大野'
                        elif kanji == '秦':
                            destination = '秦野'
                    else:
                        destination = '本厚木'
                    try:
                        time = datetime.strptime(time_str, '%H:%M')
                        time = time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                        times.append((time, destination))
                    except ValueError as e:
                        pass
                    time_str = ''
    
    nearest_times = []
    for time, destination in times:
        if time >= now:
            nearest_times.append((time, destination))
        if len(nearest_times) == 3:
            break
    
    return nearest_times


@app.route('/table')
def get_table():
    kudari_csv_file = '../odakyu/kudari_hejitsu.csv'
    kudari_nearest_times = get_kudari_nearest_times(kudari_csv_file)

    nobori_csv_file = '../odakyu/nobori_hejitsu.csv'
    nobori_nearest_times = get_nobori_nearest_times(nobori_csv_file)

    global kudari_table
    kudari_table = []
    print("下り")
    for kudari_time, kudari_destination in kudari_nearest_times:    
        kudari_table.append({'出発時刻': kudari_time.strftime("%H:%M"), '目的地': kudari_destination})

    print("上り")
    global nobori_table
    nobori_table = []
    for nobori_time, nobori_destination in nobori_nearest_times:    
        nobori_table.append({'出発時刻': nobori_time.strftime("%H:%M"), '目的地': nobori_destination})

    now_time = datetime.now().strftime("%H:%M:%S")
    return render_template('table.html', kudari_table=kudari_table, nobori_table=nobori_table, now_time=now_time)


@app.route('/')
def display_train_info():
    update_train_info()
    return render_template('app.html', train_info=train_info)




if __name__ == '__main__':
    update_train_info()
    app.run(port=8000)

    while True:
        time(300)
        app.run(port=8000)
