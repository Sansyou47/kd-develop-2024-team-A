from flask import Blueprint, render_template, request, redirect,session
from function import mysql

#やってること
#まずログインチェックを行う
#してるなら弁当点数履歴確認に必要な情報をDBから渡す
#戻り値はlunch_score
#してないならログイン画面に飛ばす


# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("mypage", __name__)
#ログインしているIDをセッションから取得
user_id = session['user_id']
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        ID = request.form.get('user_id')
        try:
            #取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute('SELECT * from lunch_score where user_id = %s', (ID,))
            #lunch_scoreに入れる
            lunch_score = mysql.cur.fetchall()
        except Exception as e:
            return str(e)
        #lunch_scoreの情報をmypage.htmlに渡す
        return render_template('mypage.html',lunch_score=lunch_score)
    else:
        return redirect('/signup')
