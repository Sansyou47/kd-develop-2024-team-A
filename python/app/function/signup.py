from flask import Blueprint, render_template, request, redirect, url_for,session
from werkzeug.security import generate_password_hash
from function import mysql
import re

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("signup", __name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    email = ''
    name = ''
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        secret_question = request.form.get('secret_question')
        secret_answer = request.form.get('secret_answer')

        # メールアドレスの形式確認
        if email.count('@') != 1:
            error = '正しくメールアドレスを入力してください'
        
        # メールアドレスの重複確認
        if not error:
            mysql.cur.execute('SELECT * FROM users where email = %s', (email,))
            user = mysql.cur.fetchone()
            if user:
                error = 'このメールアドレスは既に登録されています'
        
        # ユーザー名の長さ確認
        if not error:
            if len(name) < 2:
                error = 'ユーザー名は2文字以上である必要があります'
        if not error:
            if len(name) > 10:
                error = 'ユーザー名は10文字以内である必要があります'

        # パスワードの長さと文字確認
        if not error:
            if len(password) < 8:
                error = 'パスワードは8文字以上である必要があります'
            elif not re.search(r'\d', password):
                error = 'パスワードには少なくとも1つの数字が含まれている必要があります'
            elif not re.search(r'[a-zA-Z]', password):
                error = 'パスワードには少なくとも1つの英字が含まれている必要があります'
            elif password != password_confirmation:
                error = 'パスワードとパスワード確認が一致しません'
            else:
                hashed_password = generate_password_hash(password)

        # 秘密の質問があるかの確認
        if not error:
            if secret_question == '0':
                error = '質問を選択してください'

        # 秘密の質問の答えの長さ確認
        # 秘密の質問の答えはひらがな、カタカナ、漢字、英数字のみ許可かつ2文字以上15文字以内
        if not error:
            if len(secret_answer) < 2:
                error = '答えは2文字以上である必要があります'
            elif len(secret_answer) > 15:
                error = '答えは15文字以内である必要があります'
            elif not re.match(r'^[ぁ-んァ-ン一-龥a-zA-Z0-9]+$', secret_answer):
                error = '答えにはひらがな、カタカナ、漢字、英数字のみ使用できます'

        # なんも問題なかったら新規登録
        if not error:
            try:
                # 新規登録のSQL
                    sql = 'INSERT INTO users (name, password, email, secret_question, secret_answer) VALUES (%s, %s, %s, %s, %s)'
                    mysql.cur.execute(sql, (name, hashed_password, email, secret_question, secret_answer))
                    mysql.conn.commit()
                    return render_template('login.html')
            except Exception as e:
                if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                    return
                else:
                    title = 'Oops！エラーが発生しちゃった！😭'
                    message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                    return render_template('error.html', title=title, message=message, error=e)
        

    return render_template('signup.html', error=error, email=email, name=name)

@app.route('/secret_question', methods=['GET', 'POST'])
def secret_question():
    error = None
    secret_question_result = None
    secret_answer_result = None

    if request.method == 'POST':
        email = request.form.get('email')
        secret_question = request.form.get('secret_question')
        secret_answer = request.form.get('secret_answer')
        try:
            # メールアドレスの形式確認
            if email.count('@') != 1:
                error = '正しくメールアドレスを入力してください'
            # メールアドレスが存在するか確認
            mysql.cur.execute('SELECT secret_question, secret_answer FROM users WHERE email = %s', (email,))
            result = mysql.cur.fetchone()
            if not result:
                error = 'このメールアドレスは登録されていません'
            else:
                # resultからsecret_question_resultとsecret_answer_resultを格納
                secret_question_result = result[0]
                secret_answer_result = result[1]
                # メールアドレスと秘密の質問が一致するか確認
                if secret_question_result != secret_question:
                    error = '秘密の質問が一致しません'
                
                # 秘密の質問と答えが一致するか確認
                if not error:
                    if secret_answer_result != secret_answer:
                        error = '秘密の質問の答えが一致しません'
                
                # パスワード再設定ページに遷移
                if not error:
                    return render_template('reset_password.html', email=email)
        except Exception as e:
            if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                return
            else:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
        
    return render_template('secret_question.html', error=error)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        # emailが存在しなければエラーを返す
        if not email:
            print(email)
            title = 'Oops！エラーが発生しちゃった！😭異端者はカエレ！'
            message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
            return render_template('error.html', title=title, message=message)
        # パスワードの長さと文字確認
        if not error:
            if len(password) < 8:
                error = 'パスワードは8文字以上である必要があります'
            elif not re.search(r'\d', password):
                error = 'パスワードには少なくとも1つの数字が含まれている必要があります'
            elif not re.search(r'[a-zA-Z]', password):
                error = 'パスワードには少なくとも1つの英字が含まれている必要があります'
            elif password != password_confirmation:
                error = 'パスワードとパスワード確認が一致しません'
            else:
                hashed_password = generate_password_hash(password)
        # パスワード再設定
        if not error:
            try:
                sql = 'UPDATE users SET password = %s WHERE email = %s'
                mysql.cur.execute(sql, (hashed_password, email))
                mysql.conn.commit()
                # 再設定が完了しているDBと比較して確認
                mysql.cur.execute('SELECT password FROM users WHERE email = %s', (email,))
                user = mysql.cur.fetchone()
                if user[0] == hashed_password:
                    title = 'パスワード再設定完了！🎉'
                    message = 'ログインページに戻って新しいパスワードでログインしてね！'
                    return render_template('error.html', title=title, message=message)
                else:
                    title = 'Oops！エラーが発生しちゃった！😭'
                    message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してねSHINE。'
                    return render_template('error.html', title=title, message=message, error=e)
            except Exception as e:
                if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                    return
                else:
                    title = 'Oops！エラーが発生しちゃった！😭'
                    message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                    return render_template('error.html', title=title, message=message, error=e)
    return render_template('reset_password.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)