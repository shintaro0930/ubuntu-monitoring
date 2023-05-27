import datetime
import jpholiday



def isBizDay(DATE):
    Date = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        #休日
        print('今日は休日です')        
        return 0
    else:
        #平日
        print('今日は平日です')        
        return 1


DATE = "yyyymmdd" # 日付は８桁文字列の形式
current_date = str(datetime.datetime.now().date()).replace('-', '')

print(type(current_date))
print(current_date)
print(isBizDay(current_date))