from flask import Blueprint, render_template, request, redirect, url_for,session
from werkzeug.security import generate_password_hash
from function import mysql
import re,random,os,smtplib,datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("signup", __name__)

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

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

        # なんも問題なかったら新規登録
        if not error:
            try:
                # 新規登録のSQL
                    sql = 'INSERT INTO users (name, password, email) VALUES (%s, %s, %s)'
                    mysql.cur.execute(sql, (name, hashed_password, email))
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

@app.route('/certification/authentication_key/reset_password', methods=['GET', 'POST'])
def reset_password():
    error = None
    if request.method == 'POST':
        # sessionからemailを取得
        email = session.get('email_log')
        # sessionからemailがなかったらエラーを返す
        if not email:
            title = 'Oops！エラーが発生しちゃった！'
            message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
            return render_template('error.html', title=title, message=message)
        # パスワードの取得
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        # emailで認証コードが1時間以上立っていたらsessionを削除してもう一度認証コードを取得してもらう
        mysql.cur.execute('SELECT create_date FROM certification_key WHERE email = %s', (email,))
        result = mysql.cur.fetchone()
        # result[0]がdatetimeオブジェクトであることを確認しないとエラッタ
        if result and isinstance(result[0], datetime.datetime):
            time_difference = datetime.datetime.now() - result[0]
            if time_difference.total_seconds() > 600:
                mysql.cur.execute('DELETE FROM certification_key WHERE email = %s', (email,))
                session.pop('email_log', None)
                title = 'Oops！エラーが発生しちゃった！😭'
                message = '認証コードの有効期限が切れました。もう一度認証コードを取得してください。'
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
                # ここでsessionのemailを削除
                session.pop('email_log', None)
                mysql.cur.execute('DELETE FROM certification_key WHERE email = %s', (email,))
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
# CREATE TABLE certification_key (
#     email VARCHAR(255) PRIMARY KEY,
#     ce_key INT NOT NULL,
#     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
@app.route('/certification', methods=['GET', 'POST'])
def certification():
    # 認証ページ
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        # メールアドレスの形式確認
        if email.count('@') != 1:
            error = '正しくメールアドレスを入力してください'
        # メールアドレスの重複確認
        if not error:
            mysql.cur.execute('SELECT email FROM users where email = %s', (email,))
            result = mysql.cur.fetchone()
        # メールアドレスが存在しなければエラーを返す
            if not result:
                error = 'このメールアドレスは登録されていません'
            else:
                email=result[0]

        if not error:
            # 認証コードを数字6文字ランダム生成
            random_code = random.randint(100000, 999999)
            # 既に認証コードが存在していたら削除
            mysql.cur.execute('SELECT email FROM certification_key where email = %s', (email,))
            result = mysql.cur.fetchone()
            if result:
                mysql.cur.execute('DELETE FROM certification_key WHERE email = %s', (email,))
            # メアドと共にDBに保存
            mysql.cur.execute('INSERT INTO certification_key (email, ce_key) VALUES (%s, %s)', (email, random_code))
            # 認証コードをメアドに送信
            # メール送信元
            from_email = ADMIN_EMAIL
            # メール送信元のパスワード
            password = ADMIN_PASSWORD
            # SMTPサーバー
            port = 587
            # メール送信先
            to_email = email
            # メール件名
            subject = 'Snapscöreのパスワードリセット認証コードのお知らせ'
            # メール本文
            message = "あなたの認証コードは" + str(random_code) + "です。身に覚えがない場合は無視してください。"
            # メール送信
            msg = create_msg(from_email, to_email, subject, message)
            send_mail(to_email, msg, port, from_email, password)
            session['email_key'] = email
            return redirect(url_for('signup.authentication_key'))

    return render_template('certification.html', error=error)

def create_msg(from_addr, to_addr, subject, body):
    msg = MIMEText(body.encode('iso-2022-jp'), 'plain', 'iso-2022-jp')
    msg["From"] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = formatdate()
    return msg

def send_mail(to_addrs, msg, PORT, FROM, PASSWORD):
    smtpobj = smtplib.SMTP('smtp.gmail.com', PORT)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM, PASSWORD)
    smtpobj.sendmail(FROM, to_addrs, msg.as_string())
    smtpobj.close()

@app.route('/certification/authentication_key', methods=['GET', 'POST'])
def authentication_key():
    email = session.get('email_key')
    result = None
    if not email:
        title = 'Oops！エラーが発生しちゃった！'
        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
        return render_template('error.html', title=title, message=message)
    error = None
    if request.method == 'POST':
        key = request.form.get('auth_code')
        if not key:
            error = '認証コードを入力してください'
        # 数字以外ならエラーを返す
        if not error:
            if not key.isdecimal():
                error = '認証コードは数字6文字で入力してください'
        if not error:
            mysql.cur.execute('SELECT ce_key FROM certification_key WHERE email = %s', (email,))
            result = mysql.cur.fetchone()
            if int(key) != result[0]:
                error = '認証コードが一致しません'
            else:
                mysql.cur.execute('DELETE FROM certification_key WHERE email = %s', (email,))
                session['email_log'] = email
                session.pop('email_key', None)
                return redirect(url_for('signup.reset_password'))

    return render_template('authentication.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)