from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from function import mysql
import re

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("signup", __name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        # メールアドレスの形式チェチェ
        if email.count('@') != 1:
            error = 'メールアドレスには「@」が1つ含まれている必要があります'
        
        # メールアドレスの重複チェチェ
        if not error:
            mysql.cur.execute('SELECT * FROM users where email = %s', (email,))
            user = mysql.cur.fetchone()
            if user:
                error = 'このメールアドレスは既に登録されています'
        
        # ユーザー名の長さチェチェ
        if not error:
            if len(name) < 2 or len(name) > 16:
                error = 'ユーザー名は2文字以上16文字以下である必要があります'

        # パスワードの長さと文字チェチェ
        if not error:
            if len(password) < 8 or len(password) > 16:
                error = 'パスワードは8文字以上16文字以下である必要があります'
            elif not re.search(r'\d', password):
                error = 'パスワードには少なくとも1つの数字が含まれている必要があります'
            elif not re.search(r'[a-zA-Z]', password):
                error = 'パスワードには少なくとも1つの英字が含まれている必要があります'
            elif password != password_confirmation:
                error = 'パスワードとパスワード確認が一致しません'
            else:
                hashed_password = generate_password_hash(password)

        # なんも問題なかったら新規登録
        if not error:
            try:
                # 新規登録のSQL
                    sql = 'INSERT INTO users (name, password, email) VALUES (%s, %s, %s)'
                    mysql.cur.execute(sql, (name, hashed_password, email))
                    mysql.conn.commit()
                    return render_template('login.html')
            except Exception as e:
                return render_template('err.html')
                # return str(e)

    return render_template('signup.html', error=error)

# ページ表示用のデバック
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)