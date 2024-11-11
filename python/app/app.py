from flask import Flask, render_template, request, redirect, url_for,session, session
from function import mysql
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from function import blueprint_demo, gemini_demo, easter_egg, judgment_color, Shortage, remove_background, debug,image_show,mypage, mysql,signup,ranking,guide,x
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
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
app.register_blueprint(image_show.app) #サムネの画像表示用
app.register_blueprint(debug.app) #デバック用
app.register_blueprint(signup.app)
app.register_blueprint(mypage.app)
app.register_blueprint(ranking.app)
app.register_blueprint(guide.app)
app.register_blueprint(x.app)

#session用の秘密鍵
app.secret_key = token_hex(128)

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
    mysql.cur.execute("SELECT * FROM users WHERE id = %s", (user_id))
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

@app.route('/login', methods=["GET", "POST"])
def login():
    #現在有効なログイン情報を持っているならトップページにリダイレクト
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        mysql.cur.execute("SELECT * FROM users WHERE email = %s", (email))
        user = mysql.cur.fetchone()

        # パスワードをハッシュ値と照合して一致した場合
        if user and check_password_hash(user[2], password):
            uid = user[0]
            login_user(User(uid))
            # ユーザー情報を取得
            mysql.cur.execute("SELECT name FROM users WHERE id = %s", (uid))
            userInfo = mysql.cur.fetchone()
            # セッションに情報を格納
            session['user_id'] = uid
            session['user_name'] = userInfo[0]
            session['user_email'] = email
            return redirect('/')
        else:
            error_message = "ユーザーIDまたはパスワードが間違っています。"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')
    

@app.route('/logout')
def logout():
    #セッション情報の削除
    session.clear()
    #Flaskログアウト
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")