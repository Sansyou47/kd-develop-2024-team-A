from flask import Blueprint, render_template, request, redirect, session
from function import mysql
import base64, os, json

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("x", __name__)
# CREATE TABLE lunch_score (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     score INT NOT NULL,
#     lunch_image_name VARCHAR(255) NOT NULL,
#     use_gemini BOOLEAN DEFAULT TRUE,
#     is_not_lunch BOOLEAN DEFAULT FALSE,
#     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     all_result text,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );

# color_score_inc=lunch_score,DBのscore
# data_uri=bento_url,とりあえずあとでos使って画像を持ってくる
# color_point=color_point,★
# color_point_name_code=color_point_name_code,★
# color_point_name_jp=color_point_name_jp,★
# colors_code=colors_code,★
# colors_per=colors_per,★
# color_graph=color_graph,★
# nakai_color_zen=nakai_color_zen,★
# response=gemini_response,★
# Shortage_result=Shortage_result★
# データベースからすべてのデータを取得して完了

# エンコードされたIDをデコードする関数ｩ
def decode_id(encoded_id):
    try:
        decoded_bytes = base64.urlsafe_b64decode(encoded_id)  # Base64デコード
        return decoded_bytes.decode('utf-8')  # バイト列を文字列に変換
    except Exception as e:
        raise ValueError("例外が発生しました。") from e
@app.route('/x', methods=['GET'])
def x():
    lunch_score = None
    data_uri = None
    color_point = None
    color_point_name_code = None
    color_point_name_jp = None
    colors_code = None
    colors_per = None
    color_graph = None
    nakai_color_zen = None
    gemini_response = None
    Shortage_result = None
    image_name = None

    try:
        if request.method == 'GET':
            session.clear()
            # エンコードされたIDを取得
            encoded_id = request.args.get('id')
            # IDをデコード
            id = decode_id(encoded_id)
            # SQL文で対象のデータを取得
            sql = 'SELECT score, all_result FROM lunch_score WHERE id = %s'   
            # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute(sql, (id,))
            result = mysql.cur.fetchone()

            if result:
                lunch_score = int(result[0])
                all_result = json.loads(result[1])
                color_point = all_result[0]
                color_point_name_code = all_result[1]
                color_point_name_jp = all_result[2]
                colors_code = all_result[3]
                colors_per = all_result[4]
                color_graph = all_result[5]
                nakai_color_zen = all_result[6]
                gemini_response = all_result[7]
                Shortage_result = all_result[8]
            
            # 画像処理
            sql = 'SELECT lunch_image_name FROM lunch_score WHERE id = %s'
            mysql.cur.execute(sql, (id,))
            result = mysql.cur.fetchone()
            for row in result:
                image_name = row
            image_path = os.path.join(os.path.dirname(__file__),'..','rmbg', 'original', f'{image_name}.jpeg')
            try:
                with open(image_path, "rb") as image:
                    # 画像を読み込みbase64にエンコード
                    image_data = image.read()
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    # 画像をdataURIに変換
                    data_uri = f"data:image/jpeg;base64,{encoded_image}"
                    print(image_name)
                    print(image_path)
            except Exception as e:
                if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                    return
                else:
                    title = 'Oops！エラーが発生しちゃった！😭'
                    message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                    return render_template('error.html', title=title, message=message, error=e)
        return render_template(
        'image_result.html',
        id=id,
        color_score_inc=lunch_score,
        data_uri=data_uri,
        color_point=color_point,
        color_point_name_code=color_point_name_code,
        color_point_name_jp=color_point_name_jp,
        colors_code=colors_code,
        colors_per=colors_per,
        color_graph=color_graph,
        nakai_color_zen=nakai_color_zen,
        response=gemini_response,
        Shortage_result=Shortage_result
    )
    except Exception as e:
        if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
            return
        else:
            if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                return
            else:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)