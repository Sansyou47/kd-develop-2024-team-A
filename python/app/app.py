from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from function import blueprint_demo, gemini_demo, easter_egg, judgment_color, Shortage, remove_background, debug, mysql
import os

app = Flask(__name__)

# セッション情報を暗号化するためのキーを設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager(app)
login_manager.login_view = 'login' 

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(blueprint_demo.app)
app.register_blueprint(gemini_demo.app)
app.register_blueprint(easter_egg.app)
app.register_blueprint(judgment_color.app)
app.register_blueprint(Shortage.app)
app.register_blueprint(remove_background.app)
app.register_blueprint(debug.app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        
# ログイン中のユーザーIDを取得する関数
def get_uid():
    # ユーザーIDを取得し、戻り値に設定する（メアドから"@"以降を削除する処理を追加）
    uid = str(current_user.id)
    uid = uid.split('@')[0]
    return uid

@login_manager.user_loader
def load_user(user_id):
    mysql.cur.execute("SELECT * FROM users WHERE userId = %s", (user_id))
    user = mysql.cur.fetchone()
    if user:
        return User(user_id)
    else:
        return None

# インデックスルート
@app.route('/')
def index():
    #クッキーから情報を取得
    access = request.cookies.get('access')
    
    #クッキーが無ければaccessにfalseを代入
    if access != 'true':
        access = 'false'
    
    #intro.htmlにaccessを渡す
    return render_template('intro.html', access=access)

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userid = request.form["userid"]
        password = request.form["password"]
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE userId = %s", (userid))
        user = cursor.fetchone()
        
        # パスワードをハッシュ値と照合して一致した場合
        if user and check_password_hash(user[4], password):
            login_user(User(userid))
            uid = str(current_user.id)
            # ユーザー情報を取得
            cursor.execute("SELECT userNumber, userName, gitAccount, userIcon FROM users WHERE userId = %s", (userid))
            userInfo = cursor.fetchone()
            # セッションに情報を格納
            session['user_id'] = uid
            session['user_name'] = userInfo[1]
            session['git_account'] = userInfo[2]
            session['now_sprint'] = 1
            if userInfo[3] is None:
                session['user_icon'] = "default.svg"
            else:
                session['user_icon'] = userInfo[3]
            return redirect('/select_project')
        else:
            error_message = "ユーザーIDまたはパスワードが間違っています。"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")