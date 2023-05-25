import csv
from datetime import datetime

# 現在の時刻を取得
current_time = datetime.now().time()

# 時刻の差を計算するための関数


def time_difference(time1, time2):
    if time1 <= time2:
        return (time2.hour - time1.hour) * 60 + (time2.minute - time1.minute)
    else:
        return (24 - time1.hour + time2.hour) * 60 + (time2.minute - time1.minute)

# 直近3本の電車を取得する関数

def get_recent_trains(data, current_time):
    # 時刻の差を計算してデータに追加
    for row in data:
        train_time = datetime.strptime(row[0], '%H時').time()
        row.append(time_difference(current_time, train_time))

    # 時刻の差でソート
    sorted_data = sorted(data, key=lambda x: x[2])

    # 直近3本の電車を取得
    recent_trains = sorted_data[:3]

    return recent_trains


# sample.csvからデータを読み込む
with open('kudari_hejitsu.csv', 'r') as file:
    csv_reader = csv.reader(file)
    train_data = [row for row in csv_reader]

    # 直近3本の電車を取得
    recent_trains = get_recent_trains(train_data, current_time)

    # 結果を表示
    for train in recent_trains:
        print(','.join(train[:2]))  # 時刻とデータをカンマで結合して表示
