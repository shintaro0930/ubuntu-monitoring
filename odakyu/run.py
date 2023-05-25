import csv
from datetime import datetime
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

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

nobori_csv_file =  'nobori_hejitsu.csv'
kudari_csv_file = 'kudari_hejitsu.csv'
nobori_nearest_times = get_nobori_nearest_times(nobori_csv_file)
kudari_nearest_times = get_kudari_nearest_times(kudari_csv_file)

print("現在の時間以降で最も近い3つの時刻と行き先:")
print('===下り===')
for time, destination in kudari_nearest_times:
    print(f'{time.strftime("%H:%M")}  {destination}行き')

print('===上り===')
for time, destination in nobori_nearest_times:
    print(f'{time.strftime("%H:%M")}  {destination}行き')

