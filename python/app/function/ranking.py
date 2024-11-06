# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from function import mysql
from datetime import datetime, timedelta
import base64, os

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("ranking", __name__)

# データベースの中身
# drop table if exists lunch_score;
# -- スコアテーブル
# -- "is_not_lunch"がtrueの場合は写真内に弁当が含まれていないと判断されたことを意味する
# CREATE TABLE lunch_score (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     score INT NOT NULL,
#     lunch_image_name VARCHAR(255) NOT NULL,
#     use_gemini BOOLEAN DEFAULT TRUE,
#     is_not_lunch BOOLEAN DEFAULT FALSE,
#     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );

# drop table if exists users;
# -- ユーザーテーブル
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     password VARCHAR(1024) NOT NULL,
#     email VARCHAR(255) UNIQUE NOT NULL,
#     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
def no_image():
    # 画像がない場合の画像を表示
    image_path = os.path.join(os.path.dirname(__file__),'..','static', 'no_image.jpeg')
    with open(image_path, "rb") as image:
        image_data = image.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        no_image = f"data:image/jpeg;base64,{encoded_image}"
    return no_image

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
        # resultのscoreが高い順に並び替え
        result = sorted(result, key=lambda x: x[0], reverse=True)
        # resultのデータを上から3つ取得
        result_mittu = result[:3]
        # result_mittuが3つ以下の場合はないよ画像を挿入のリストを作成ここから月曜日新しいタスク書いとこうね
        # result_mittuの長さに応じた処理
        # result_mittu_length = len(result_mittu)
        # if result_mittu_length < 3 :
        #     # 3つ以下の場合はno_image()を挿入
        #     for i in range(3 - result_mittu_length):
        #         socre = i[0]
        #         image_name = i[1]
        #         user_name = 'まだ投稿がありません'
        #     result_mittu.append((0, no_image(), 'No Image'))
        #     no_image = no_image()

        ranking_reselt = []
        # 画像を読み込み
        for row in result_mittu:
            score = row[0]      # 1番目のデータの点数を取得
            image_name = row[1] # 2番目のデータの画像名を取得
            user_name = row[2]
            # 以下mypageからのコピペ
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