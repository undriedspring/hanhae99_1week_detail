from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "../static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
db = client.hanghae99_chapter1


# index .main
@app.route('/')
def details():
    return render_template('details.html')

@app.route("/movie/<movie_id>/comment", methods=["POST"])
def comment(movie_id):
    """
    여기서 댓글 기능 구현
    """
    if request.method == "POST":
        token_receive = request.cookies.get("mytoken")
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        username = (payload["id"])
        movie_id_receive = movie_id
        comment_receive = request.form["comment_give"]

        doc = {
            "user_id": username,
            "movie_id": movie_id_receive,
            "comment": comment_receive,
        }
        db.comments.insert_one(doc)
        return jsonify({"result": "success", "msg": "댓글를 추가했습니다."})


@app.route("/movie/<movie_id>/comment/delete", methods=["POST"])
def del_comment(movie_id):
    if request.method == "POST":

        token_receive = request.cookies.get("mytoken")
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = (payload["id"])

        comment_receive = request.form["comment_give"]
        target_comment = db.comments.find_one({"user_id": username, "movie_id": movie_id, "comment": comment_receive})

        if target_comment is not None:
            db.comments.delete_one({"user_id": username, "movie_id": movie_id, "comment": comment_receive})

            return jsonify({"result": "success", "msg": "댓글 삭제"})
        else:
            return jsonify({"result": "fail", "msg": "다른 사람의 댓글은 삭제할 수 없습니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)