import requests
from datetime import datetime,timedelta

now = datetime.now()
before_minute = now - timedelta(minutes=30)
date = before_minute.strftime('%Y-%m-%d-%H-%M')
temp = date.split("-")

year = temp[0]
month = temp[1]
day = temp[2]
hour = temp[3]
minute = temp[4]

today = str(year)+str(month)+str(day)
time = str(hour)+str(minute)

key = 'zCe25bd4+iOzXz+hX4cGfYCkt/JE6ch0H2MfRYXXDHaxbgpVmt/C2BSKaj5Gm2aEtJKSjSIq+RCwnkhRk2jJ1A=='
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
params ={'serviceKey' : key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : today, 'base_time' : time, 'nx' : '55', 'ny' : '127' }

response = requests.get(url, params=params)
data = response.json()

lists = data['response']['body']['items']['item']

hour = int(hour)+1;
time = str(hour)+'00'

t1h = 0
sky = ''
pty = ''
for list in lists:
    if list['category'] == "T1H" and list['fcstTime'] == time:
        t1h = list['fcstValue']
    elif list['category'] == 'SKY' and list['fcstTime'] == time:
        if list['fcstValue'] == '1':
            sky = '맑음'
        elif list['fcstValue'] == '3':
            sky = '구름많음'
        else:
            sky = '흐림'
    elif list['category'] == 'PTY' and list['fcstTime'] == time:
        if list['fcstValue'] == '0':
            pty = ''
        elif list['fcstValue'] == '1' or list['fcstValue'] == '5' or list['fcstValue'] == '6':
            pty = '비'
        elif list['fcstValue'] == '2':
            pty = '비/눈'
        elif list['fcstValue'] == '3' or list['fcstValue'] == '7':
            pty = '눈'

if pty == '':
    pty = sky














# date = '2022년4월21일'
#
# year = date.split('년')[0]
# temp = date.split('년')[1]
# month = int(temp.split('월')[0])
# if month < 10:
#     month = '0' + str(month)
# temp = date.split('월')[1]
# day = int(temp.split('일')[0])
# if day < 10:
#     day = 0 + str(day)
#
# temp = year + str(month) + str(day)
#
# current = datetime.now()
# now = current - datetime.timedelta(minutes=30)
#
# hour = now.hour
# minute = now.minute
#
# hour = int(hour)
# if hour < 10:
#     hour = '0' + str(hour)
#
# minute = int(minute)
# if minute < 10:
#     day = str(0) + str(minute)
#
# time = str(hour) + str(day)
#
# print(time, temp)