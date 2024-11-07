from flask import Blueprint, render_template, request, redirect, url_for
from function import mysql
from datetime import datetime, timedelta
import base64, os

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("ranking", __name__)

@app.route('/ranking')
def raning():
    try:
        # 今日の日付のデータを取得
        today = datetime.now()
        # 1週間前の日付を取得
        one_week_ago = today - timedelta(days=7)
        #  lunch_scoreをls、usersをuとして、score, lunch_image_name, nameを取得その時にcreate_dateが今日から1週間前のデータを取得
        sql = 'SELECT ls.score, ls.lunch_image_name, u.name FROM lunch_score ls JOIN users u ON ls.user_id = u.id WHERE ls.is_not_lunch = false AND ls.create_date BETWEEN %s AND %s'
        mysql.cur.execute(sql,(one_week_ago,today,))
        result = mysql.cur.fetchall()

        # resultのscoreが高い順に並び替えて上位3つを取得
        result = sorted(result, key=lambda x: x[0], reverse=True)
        result_mittu = result[:3]

        # result_mittuの長さに応じて不足分を補う
        while len(result_mittu) < 3:
            result_mittu.append((0, 'no_image.jpeg', "匿名"))

        ranking_reselt = []

        # 画像を読み込み
        for row in result_mittu:
            score = row[0]      # 1番目のデータの点数を取得
            image_name = row[1] # 2番目のデータの画像名を取得
            user_name = row[2]
            # データがなかったらno_imageを表示するように
            if image_name == 'no_image.jpeg':
                image_path = os.path.join(os.path.dirname(__file__),'..','static', 'images', 'no_image.jpeg')
            else:
                # 相対パスを使用して画像パスを指定
                image_path = os.path.join(os.path.dirname(__file__),'..','rmbg', 'original', f'{image_name}.jpeg')
            try:
                with open(image_path, "rb") as image:
                    # 画像を読み込みbase64にエンコード
                    image_data = image.read()
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    # 画像をdataURIに変換
                    ranking_bento_url = f"data:image/jpeg;base64,{encoded_image}"
                    ranking_reselt.append((score, ranking_bento_url, user_name))
            except Exception as e:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
        # ランキングをranking.htmlに渡す
        return render_template('ranking.html', ranking_reselt=ranking_reselt)
    except Exception as e:
        title = 'Oops！エラーが発生しちゃった！😭'
        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
        return render_template('error.html', title=title, message=message, error=e)

if __name__ == '__main__':
    app.run(debug=True)