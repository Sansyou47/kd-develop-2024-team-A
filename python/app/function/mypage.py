from flask import Blueprint, render_template, request, redirect,session
from function import mysql
import base64, os

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
        # ログインしているIDをセッションから取得
        try:
            sql = 'SELECT score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s'
            # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute(sql, (user_id,))
            # resultに入れる
            result = mysql.cur.fetchall()
            # 画像を読み込み
            mypage_result_zen = []
            for row in result:
                score = row[0]      # 1番目のデータの点数を取得
                image_name = row[1] # 2番目のデータの画像名を取得
                create_date = row[2] # 3番目のデータの日付を取得
                # 相対パスを使用して画像パスを指定
                image_path = os.path.join(os.path.dirname(__file__), '..', 'rmbg', 'original', f'{image_name}.jpeg')
                try:
                    with open(image_path, "rb") as image:
                        # 画像を読み込みbase64にエンコード
                        image_data = image.read()
                        encoded_image = base64.b64encode(image_data).decode('utf-8')
                        # 画像をdataURIに変換
                        bento_url = f"data:image/jpeg;base64,{encoded_image}"
                        mypage_result_zen.append((score, bento_url, create_date))
                except FileNotFoundError:
                    mypage_result_zen.append((None, None, None))
        except Exception as e:
            print(f"Error: {e}")  # デバッグメッセージ
            return str(e)
        # lunch_scoreの情報をmypage.htmlに渡す
        return render_template('mypage.html', mypage_result_zen, user_id=user_id)
    else:
        return redirect('/login')
