from flask import Blueprint, Flask, render_template, request, redirect, url_for, session
from function import mysql
from werkzeug.security import check_password_hash, generate_password_hash

app = Blueprint('login', __name__)

@app.route('/login', methods=["GET", "POST"])
def login():
    #現在有効なログイン情報を持っているならトップページにリダイレクト
    if 'user_id' in session:
        return redirect('/')
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        #ログイン後のリダイレクト先を取得
        url = request.form["url"]
        mysql.cur.execute("SELECT * FROM users WHERE email = %s", (email))
        user = mysql.cur.fetchone()

        # パスワードをハッシュ値と照合して一致した場合
        if user and check_password_hash(user[2], password):
            uid = user[0]
            # ユーザー情報を取得
            mysql.cur.execute("SELECT name FROM users WHERE id = %s", (uid))
            userInfo = mysql.cur.fetchone()
            # セッションに情報を格納
            session['user_id'] = uid
            session['user_name'] = userInfo[0]
            session['user_email'] = email
            # 30日間セッションを保持
            session.permanent = True
            # ログインした先のurlを設定する。なければルートに
            if url:
                return redirect(url)
            return redirect('/')
        else:
            error_message = "ユーザーIDまたはパスワードが間違っています。"
            return render_template('login.html', error_message=error_message, url=url)
    else:
        return render_template('login.html')
    

@app.route('/logout')
def logout():
    #セッション情報の削除
    session.clear()
    return redirect('/')

#ログインチェック関数
def check(url):
    if 'user_id' in session:
        return None
    else:
        return render_template('login.html', url=url)
    