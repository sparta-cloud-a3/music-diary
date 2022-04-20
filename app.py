from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bs4 import BeautifulSoup
import datetime
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.music_diary


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write')
def write():
    return render_template('write_diary.html')


@app.route('/diaries', methods=['GET'])
def listing():
    diary_list = list(db.post.find({}, {'_id': False}))

    return jsonify({'diaries': diary_list})


@app.route('/diaries/search', methods=['GET'])
def searchlisting():
    query_receive = request.args.get('query')
    print(query_receive)
    lists = list(db.post.find({'title': {'$regex': query_receive}}, {'_id': False}))
    print(lists)

    return render_template('search.html', query=query_receive, orders=lists)


# return jsonify({'all_lists':lists , 'msg':query_receive})

@app.route('/diaries', methods=['POST'])
def saving():
    title = request.form['title_give']
    writer = request.form['writer_give']
    content = request.form['content_give']
    url = request.form['url_give']
    date = datetime.date.strftime(datetime.date.today(), "%Y년%m월%d일")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    album_art = soup.select_one('meta[property="og:image"]')['content']
    music_title = soup.select_one('meta[property="og:title"]')['content']

    doc = {
        'title': title,
        'writer': writer,
        'album_art': album_art,
        'music_title': music_title,
        'content': content,
        'date': date
    }

    db.post.insert_one(doc)

    return jsonify({'msg': '일기 작성 완료!'})


# @app.route('/diaries/view', methods=['GET'])
# def showReview():
#     query_receive = request.args.get('query')
#     list_one = list(db.list.find_one({'title':query_receive},{'_id':False}))
#     return render_template('view.html', search_one=list_one)
#     #return jsonify({'all_lists':lists, 'msg':'list 불러왔지롱'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

# @app.route('/memo', methods=['GET'])
# def listing():
#     articles = list(db.articles.find({}, {'_id': False}))
#     return jsonify({'all_articles':articles})
