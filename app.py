from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
client = MongoClient('mongodb+srv://test:sparta@cluster0.atfonxh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

#HTML 화면 등록하기
@app.route('/')
def home():
    return render_template('lyrics_create.html')

@app.route("/toy_27", methods=["POST"])
def homework_post():
    title_receive = request.form['title_give']
    artist_receive = request.form['artist_give']
    image_receive = request.form['image_give']
    lyrics_receive = request.form['lyrics_give']
    password_receive = request.form['password_give']

    doc = {
        'title':title_receive,
        'artist':artist_receive,
        'image':image_receive,
        'lyrics':lyrics_receive,
        'password':password_receive
    }
    db.toy_27.insert_one(doc)

    return jsonify({'msg':'등록 완료'})

# HTML 화면 보여주기
# @app.route('/')
# def home():
#     return render_template('lylics_list.html')

# @app.route('/battle_create')
# def battle_create():
#     return render_template('battle_create.html')
#
# @app.route('/battle_zone')
# def battle_zone():
#     return render_template('battle_zone.html')

# 가사모음 페이지
# @app.route("/movie", methods=["POST"])
# def movie_post():
#     url_receive = request.form['url_give']
#     star_receive = request.form['star_give']
#     comment_receive = request.form['comment_give']
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url_receive, headers=headers)
#
#     soup = BeautifulSoup(data.text, 'html.parser')
#
#     title = soup.select_one('meta[property="og:title"]')['content']
#     image = soup.select_one('meta[property="og:image"]')['content']
#     desc = soup.select_one('meta[property="og:description"]')['content']
#
#     doc = {
#         'title':title,
#         'image':image,
#         'desc':desc,
#         'star':star_receive,
#         'comment':comment_receive
#     }
#     db.movies.insert_one(doc)
#
#     return jsonify({'msg':'저장 완료띠!'})
#
# @app.route("/movie", methods=["GET"])
# def movie_get():
#     movie_list = list(db.movies.find({}, {'_id': False}))
#     return jsonify({'movies':movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)