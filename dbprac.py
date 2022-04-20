from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 저장 - 예시
# doc = {'name': '타이틀3',
#        'address': '2022/03/02',
#        'img-url':'https://cdnimg.melon.co.kr/cm2/album/images/106/00/854/10600854_20210430113134_500.jpg?4c03c0d724197f49e1f50b922beb9ebe/melon/resize/282/quality/80/optimize'
#        }
db.music.update_one({'name':'타이틀3'},{'$set':{'img-url':'https://cdnimg.melon.co.kr/cm2/album/images/106/00/854/10600854_20210430113134_500.jpg?4c03c0d724197f49e1f50b922beb9ebe/melon/resize/282/quality/80/optimize'}})

#db.music.insert_one(doc)