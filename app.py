import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from datetime import datetime

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jepg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb+srv://test:sparta@cluster0.kythmsg.mongodb.net/?retryWrites=true&w=majority')
db = client.lylics_Project



# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/lyrics_create')
def lyrics_create():
    return render_template('lyrics_create.html')


@app.route('/lyrics_list')
def lyrics_list():
    return render_template('lyrics_list.html')

# 'main' 관련 코드
@app.route("/main/get", methods=["GET"])
def gasa_get():
    gasa_list = list(db.project27.find({},{'_id':False}))
    return jsonify({'gasa': gasa_list})


# 'lyrics_list.html' 관련 코드

# 가사 가져오기
@app.route("/api/sub_create", methods=["GET"])
def card_get():
    card_list = object_string(list(db.project27.find({}).sort('like', -1)))
    return jsonify({'cards': dumps(card_list)})

# 가사 삭제하기
@app.route('/api/sub_delete', methods=['POST'])
def delete_card():
    id_receive = request.form['id_give']
    db.project27.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({'msg': '가사가 삭제되었습니다.'})

# 좋아요 수 늘리기
@app.route('/api/like', methods=['POST'])
def like_comment():
    artist_receive = request.form['artist_give']

    target_id = db.project27.find_one({'artist': artist_receive})
    current_like = target_id['like']

    new_like = current_like + 1

    db.project27.update_one({'artist': artist_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# 'lyrics_create.html' 관련 코드
# 가사리스트 생성하기
@app.route('/api/sub_create', methods=['POST'])
def sub_create():
    title_receive = request.form['title_give']
    artist_receive = request.form['artist_give']
    lyrics_receive = request.form['lyrics_give']
    pw_receive = request.form['pw_give']

    file_len = len(request.files)
    # file_len 이 0이면 JS에서 파일을 안보낸준 것!
    # 파일을 안보내줬으면 default 파일이름을 넘겨준다.
    if file_len == 0:
        full_file_name = 'default_img_220315.jpg'  # default 파일이름 설정
    else:
        # 파일을 제대로 전달해줬으면 파일을 꺼내서 저장하고 파일이름을 넘겨준다.
        img_receive = request.files['img_give']

        extension = img_receive.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'lyrics-file-{mytime}'
        # save_to = f'static/assets/img/challenge/{filename}.{extension}'
        # image_receive.save(save_to)
        full_file_name = f'{filename}.{extension}'

        # 토론장 이미지 업로드 하기
        path = os.path.join(app.config['UPLOAD_FOLDER'], full_file_name)
        img_receive.save(path)

    doc = {
        'title': title_receive,
        'artist': artist_receive,
        'lyrics': lyrics_receive,
        'like': 0,
        'password': pw_receive,
        'img_src': full_file_name,
    }
    db.project27.insert_one(doc)

    return jsonify({'msg': '생성되었습니다.'})


# object 값을 str로 바꾸기
def object_string(list):
    results = []
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)