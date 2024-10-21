from flask import Blueprint, render_template, request, redirect,session
from function import mysql

#やってること
#まずログインチェックを行う
#してるなら弁当点数履歴確認に必要な情報をDBから渡す
#戻り値はlunch_score
#画像ファイルから対応する画像を持ってくる
#してないならログイン画面に飛ばす


# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("mypage", __name__)
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if "user_id" in session:
        user_id = session['user_id']
        #ログインしているIDをセッションから取得
        try:
            #取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute('SELECT (score ,lunch_image_name) from lunch_score where user_id = %s', (user_id,))
            #lunch_scoreに入れる
            lunch_score = mysql.cur.fetchall()
            # 画像を読み込み
            # Imageopen = open('static/rmbg/original/lunch_score[3].jpeg', 'rb')
            # image = request.files['image']
            # # 画像を読み込みbase64にエンコード
            # image_data = image.read()

            # image.seek(0)
            # encoded_image = base64.b64encode(image_data).decode('utf-8')
            # # 画像をdataURIに変換
            # data_uri = f"data:{image.mimetype};base64,{encoded_image}"
        except Exception as e:
            return str(e)
        #lunch_scoreの情報をmypage.htmlに渡す
        return render_template('mypage.html',lunch_score=lunch_score)
    else:
        return redirect('/signup')
