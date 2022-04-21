from flask import *
from flask_pymongo import PyMongo

web_bulletin = Flask(__name__, template_folder="templates")
web_bulletin.config["MONGO_URI"] = "mongodb://localhost:27017/bulletin"
web_bulletin.config['SECRET_KEY'] = 'psswrd'

mongo = PyMongo(web_bulletin)

web_bulletin.secret_key = '사용자지정비밀번호'

@web_bulletin.route("/login", methods=['GET',"POST"])
def bulletin_write():
    if request.method == "POST" :
        email = request.form.get("email", type=str)
        name = request.form.get('name', type=str)
        pw = request.form.get('pw', type=str)

        if email == "":
            flash("이메일을 입력하세요")
            return render_template("login.html")
        elif name == "" :
            flash("닉네임을 입력하세요")
            return render_template("login.html")
        elif pw == "" :
            flash("비밀번호를 입력하세요")
            return render_template("login.html")

        signup = mongo.db.signup
        check_cnt = signup.count_documents({"email":email})
        if check_cnt > 0:
            flash("이미 있는 계정입니다")
            return render_template("login.html")

        to_db ={
            "email" : email,
            "pw" : pw,
            "name" : name
        }
        to_db_signup = signup.insert_one(to_db)
        last_signup = signup.find().sort("_id",-1).limit(5)
        for _ in last_signup :
            print(_)

        flash("회원가입을 축하합니다")
        return render_template("login.html")
    else:
        return render_template("login.html")
if __name__ == "__main__" :
    web_bulletin.run(host='0.0.0.0', debug=True, port=9999)


