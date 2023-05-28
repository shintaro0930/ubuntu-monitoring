from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import datetime
import time
import csv
import re
import jpholiday
import json



app = Flask(__name__, static_folder='static')

train_info = {}

# cssで色分けするために列車ごとのイメージカラーのインデックスを作っておく
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
    #　今日の日付を2023-05-23のような形で取得
    current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")    
    # この関数が実行された時間を12:34:56のような形で取得(それぞれ時:分:秒)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    bool_trouble = soup.find('dd', class_='trouble')
    # find('dd), class="trouble")にはできない。これはpythonが文法上でclassを持っているため。そのため、_(アンダーバー)が必要

    """
    @params

    bool_trouble(boolean) : ddタグのclass=troubleのものがある場合(これは遅延していることを表す)、51行目のif文に突入
    content(object) : pタグのオブジェクトを保持
    
    """

    if bool_trouble:
        content = bool_trouble.find('p')
        if content:
            output = {
                "date": current_date,
                "time": current_time,                
                "status": f'{text}は遅延しています！',
                "content": f'{content.text}',
                "color": get_train_color(text)
            }
        else:
            output = {
                "date": current_date,
                "time": current_time,                
                "status": f'{text}は遅延しています！',
                "content": '遅延情報が見つかりませんでした',
                "color": get_train_color(text)
            }
    else:
        output =  {
                "date": current_date,
                "time": current_time,            
                "status": f'{text}は通常運転です',
                "content": None,
                "color": get_train_color(text)
        }

    #jsonへの書き込み
    # try構文は現在のjsonファイルを持ってきて、[{key:value}, {key:value}, {key:value} ...]構造を潰さないようにしている
    file_path = f"./delay-info/{text}.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(output)

    #json.dumpはファイルへの書き込み。indent=4は各要素に対してindentを半角4つ分加えるように指定。
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4) 

    return output


# 各路線の遅延情報をYahooから取得
def update_train_info():
    current_time = datetime.datetime.now().strftime("%H時%M分")
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
            # これ以降にget_contnt('X線', 'X線のYahoo路線情報サイト')を指定すると自動でapp.htmlに反映される
        ]
    }


# 新宿方面の直近5つの時刻表を取得
def get_nobori_nearest_times(csv_file):
    """
    @params

    row(list) : 時間帯別の時刻表を保持。csvの0列目は時間を表記しており、"X時, "になっている。 詳しくはcsvファイルを見ればわかる。
    hour(str) : X時の"X"だけを取得。ぱっと見、数字でint型と思いきや、str型に注意
    minute(str) : {hour}時に対する出発時刻の"分"を保持. time_strで 11:28 のようにしている


    """


    now = datetime.datetime.now() 
    current_date = datetime.datetime.now().date()   
    # [\u4E00-\u9FFF]は数字の後ろについてる漢字を取得している。我, 松, etc.
    kanji_pattern = re.compile(r'[\u4E00-\u9FFF]')
    
    times = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                #csvの1列目は時間情報で、X時になっているので、"時"を消す
                hour = row[0].replace('時', '')
                #2列目以降のその時間帯の時刻表をいじる
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
                        time = datetime.datetime.strptime(time_str, '%H:%M')
                        time = time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                        times.append((time, destination))
                    except ValueError as e:
                        pass
                    time_str = ''
    
    #ここで、直近の時刻表を取得している
    nearest_times:list = []
    for time, destination in times:
        if time >= now:
            nearest_times.append((time, destination))
        # 5　を 3 に変更すると、直近3つになるし、 if文そのものを消すと、その日の始発から終電までを取得
        if len(nearest_times) == 5:
            break
    
    return nearest_times

# 小田原/藤沢方面の直近5つの時刻表を取得
# 詳細は117行目へ
def get_kudari_nearest_times(csv_file):
    now = datetime.datetime.now()
    current_date = datetime.datetime.now().date()
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
                        time = datetime.datetime.strptime(time_str, '%H:%M')
                        time = time.replace(year=current_date.year, month=current_date.month, day=current_date.day)
                        times.append((time, destination))
                    except ValueError as e:
                        pass
                    time_str = ''
    
    #詳しくは117行目へ
    nearest_times = []
    for time, destination in times:
        if time >= now:
            nearest_times.append((time, destination))
        if len(nearest_times) == 5:
            break
    
    return nearest_times


# 変数Dateが平日なのか休日/祝日なのかを持ってくる。
def isBizDay(DATE):
    Date = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        #休日
        return 0
    else:     
        return 1



# 生田駅の時刻表を出力
# https://localhost:8000/table にアクセスすると表示
@app.route('/table')
def get_table():
    #now_dayの変換はisBizDay()に合うように変形
    now_day = str(datetime.date.today()).replace('-', '')
    #平日か休日かでダイヤが別
    if isBizDay(now_day) == 1:
        kudari_csv_file = '../odakyu/kudari_hejitsu.csv'     
        nobori_csv_file = '../odakyu/nobori_hejitsu.csv'           
        today = '平日'
    else:
        kudari_csv_file = '../odakyu/kudari_kyujitsu.csv'     
        nobori_csv_file = '../odakyu/nobori_kyujitsu.csv'
        today = '休日'


    now_time = datetime.datetime.now().strftime("%H:%M:%S")    
    kudari_nearest_times = get_kudari_nearest_times(kudari_csv_file)
    nobori_nearest_times = get_nobori_nearest_times(nobori_csv_file)

    global kudari_table
    #関数で持ってきた直近nこ(初期値は5)の時刻および、目的地をdict型にする
    kudari_table = []
    for kudari_time, kudari_destination in kudari_nearest_times:    
        kudari_table.append({'出発時刻': kudari_time.strftime("%H:%M"), '目的地': kudari_destination})

    global nobori_table
    nobori_table = []
    for nobori_time, nobori_destination in nobori_nearest_times:    
        nobori_table.append({'出発時刻': nobori_time.strftime("%H:%M"), '目的地': nobori_destination})

    """
    htmlに渡す。その際にhtml側で変数を宣言したときに、python側の宣言とマッチさせるようにしておく

    ex.
    kudari_table=kudari_table : 左がhtmlの変数。右がこのファイルの変数。htmlでkudari_tableが宣言された際に、その変数にはこちらのkudari_tableを渡すようにしている。
    """ 
    return render_template('table.html', kudari_table=kudari_table, nobori_table=nobori_table, now_time=now_time, today=today)


# https://localhost:8000/
@app.route('/')
def display_train_info():
    update_train_info()
    return render_template('app.html', train_info=train_info)




if __name__ == '__main__':
    update_train_info()
    # ポート番号は8000番を指定
    app.run(port=8000)

    # 5分おきに更新されるように設定
    while True:
        time(300)
        app.run(port=8000)
