from flask import Blueprint, render_template, request, redirect
from function import mysql
# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("mypage", __name__)
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        try:
            mysql.cur.execute('INSERT INTO test (name, value) VALUES (%s, %s)', (name, value))
            mysql.conn.commit()
        except Exception as e:
            return str(e)
    if 3 == 3:
        return render_template('mypage.html')
    else:
        return redirect('/signup')

#まずログインチェックを行う
#してるなら弁当点数履歴確認を行う
#してないならログイン画面に飛ばす