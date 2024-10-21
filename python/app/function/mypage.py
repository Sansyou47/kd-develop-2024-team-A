from flask import Blueprint, render_template, request, redirect
from function import mysql
# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("mypage", __name__)
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        ID = request.form.get('id')
        #ログインしているIDをセッションから取得
        #取得したIDを使ってデータベースにアクセスして、弁当点数取得
        try:
            mysql.cur.execute('SELECT * score from lunch_score where id = %s', (ID))
            result = mysql.cur.fetchall()
        except Exception as e:
            return str(e)
        return redirect('mypage.html',result=result)
    else:
        return render_template('/signup')

#まずログインチェックを行う
#してるなら弁当点数履歴確認を行う
#してないならログイン画面に飛ばす