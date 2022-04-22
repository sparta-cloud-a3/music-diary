from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.music_diary


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/write')
def write():

    return render_template('write_diary.html')


@app.route('/diary/<int:id>')
def diary(id):
    diary_give = db.post.find_one({'post_id': id}, {'_id': False})

    return render_template('diary.html', diary=diary_give)


@app.route('/diaries', methods=['GET'])
def listing():
    diary_list = list(db.post.find({}, {'_id': False}).sort('_id', -1))

    return jsonify({'diaries': diary_list})


@app.route('/search', methods=['GET'])
def search_listing():
    query_receive = request.args.get('query')
    lists = list(db.post.find({'title': {'$regex': query_receive}}, {'_id': False}))

    return render_template('search.html', text=query_receive, search_posts=lists)


@app.route('/diaries', methods=['POST'])
def saving():
    if 0 >= db.post.estimated_document_count():
        post_id = 0
    else:
        post_id = list(db.post.find({}, sort=[('_id', -1)]).limit(1))[0]['post_id'] + 1

    title = request.form['title_give']
    writer = request.form['writer_give']
    content = request.form['content_give']
    url = request.form['url_give']
    now = datetime.now()
    date = now.strftime('%Y년%m월%d일')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    album_art = soup.select_one('meta[property="og:image"]')['content']
    music_title = soup.select_one('meta[property="og:title"]')['content']

    # api 호출 후 날씨 저장하는 부분
    dict = callapi()
    weather = dict['weather']
    degree = dict['degree']

    doc = {
        'post_id': post_id,
        'title': title,
        'writer': writer,
        'album_art': album_art,
        'music_title': music_title,
        'content': content,
        'date': date,
        'weather': weather,
        'degree': degree
    }

    db.post.insert_one(doc)

    return jsonify({'msg': '일기 작성 완료!'})


def callapi():
    now = datetime.now()
    before_minute = now - timedelta(hours=2)
    date = before_minute.strftime('%Y-%m-%d-%H-%M')
    temp = date.split("-")

    year = temp[0]
    month = temp[1]
    day = temp[2]
    hour = temp[3]
    minute = temp[4]

    today = str(year) + str(month) + str(day)
    time = str(hour) + str(minute)

    key = 'zCe25bd4+iOzXz+hX4cGfYCkt/JE6ch0H2MfRYXXDHaxbgpVmt/C2BSKaj5Gm2aEtJKSjSIq+RCwnkhRk2jJ1A=='
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params = {'serviceKey': key, 'pageNo': '1', 'numOfRows': '1000', 'dataType': 'JSON', 'base_date': today,
              'base_time': time, 'nx': '55', 'ny': '127'}

    response = requests.get(url, params=params)
    data = response.json()

    lists = data['response']['body']['items']['item']

    hour = int(hour) + 1;
    if hour >= 24:
        hour == '00'
    time = str(hour) + '00'

    t1h = 0
    sky = ''
    pty = ''
    for list in lists:
        if list['category'] == "T1H" and list['fcstTime'] == time:
            t1h = list['fcstValue']
        elif list['category'] == 'SKY' and list['fcstTime'] == time:
            if list['fcstValue'] == '1':
                sky = 'sunny'
            elif list['fcstValue'] == '3':
                sky = 'cloudy'
            else:
                sky = 'little_cloudy(day)'
        elif list['category'] == 'PTY' and list['fcstTime'] == time:
            if list['fcstValue'] == '0':
                pty = ''
            elif list['fcstValue'] == '1' or list['fcstValue'] == '5' or list['fcstValue'] == '6':
                pty = 'rainy'
            elif list['fcstValue'] == '2':
                pty = 'snow_rainy'
            elif list['fcstValue'] == '3' or list['fcstValue'] == '7':
                pty = 'snow'

    if pty == '':
        pty = sky

    return {'degree': t1h, 'weather': pty}


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
