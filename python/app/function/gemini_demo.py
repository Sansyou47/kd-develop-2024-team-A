import os
import base64
import concurrent.futures
import datetime
import json
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, make_response, session
import google.generativeai as genai
from function import variable, judgment_color, mysql

app = Blueprint("gemini_demo", __name__)

app.register_blueprint(judgment_color.app)

API_KEY = os.getenv('gemini_api_key')

@app.route('/intro')
def intro():
    return redirect('/')

# 画像を入力する画面に行くためのCookieなどの処理
@app.route('/takepic', methods=['GET', 'POST'])
def takepic():
    if request.method == 'POST':
        #有効時間（秒）
        age = 24 * 60 * 60
        expires = int(datetime.datetime.now().timestamp()) + age

        #レスポンスを作成
        response = make_response(render_template('image.html'))
        #クッキーの設定
        response.set_cookie('access', value='true', expires=expires)
        return response
    else:
        return redirect('/')

# 画像から何かしらの質問をする場合の処理
@app.route('/gemini/image' , methods=['GET', 'POST'])
def gemini_image():
    if request.method == 'POST':
        image = request.files['image']
        # 画像を読み込みbase64にエンコード
        image_data = image.read()

        image.seek(0)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        # 画像をdataURIに変換
        data_uri = f"data:{image.mimetype};base64,{encoded_image}"

        # チェックボックスの状態を取得
        use_gemini = 'use_gemini' in request.form
        if use_gemini:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                try:
                    future_response = executor.submit(gemini, image)  # gemini関数の実行
                    # 画像をクラスタリングし、色の名前をラベル付けまで行う
                    future_colors = executor.submit(colors_arg, image)  # colors_arg関数の実行
                    use_gemini_flag = True
                except Exception as e:
                    if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                        return
                    else:
                        title = 'Oops！エラーが発生しちゃった！😭'
                        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                        return render_template('error.html', title=title, message=message, error=e)
                
                try:
                    gemini_response = future_response.result()  # gemini関数の結果を取得
                except Exception as e:
                    if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                        return
                    else:
                        title = 'Oops！エラーが発生しちゃった！😭'
                        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                        return render_template('error.html', title=title, message=message, error=e)
                
                # 弁当の写真を認識できなかった際の処理
                if gemini_response == 'inl.' or gemini_response == 'inl':
                    is_not_lunch_flag = True
                    gemini_response = 'この写真内から弁当を認識することができませんでした。'
                else:
                    is_not_lunch_flag = False
                    
                colors_list, judged_colors_list, image_name = future_colors.result()  # colors_arg関数の結果を取得
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 画像をクラスタリングし、色の名前をラベル付けまで行う
                future_colors = executor.submit(colors_arg, image)  # colors_arg関数の実行
                use_gemini_flag = False
                is_not_lunch_flag = False
                
                colors_list, judged_colors_list, image_name = future_colors.result()  # colors_arg関数の結果を取得
                gemini_response = None

        colors_code = [item[0] for item in colors_list]
        colors_per = [float(item[1]) for item in colors_list]
        colors_name = [item[1] for item in judged_colors_list]
        result = []
        for i in range(len(judged_colors_list)):
            result.append([colors_code[i], colors_per[i], colors_name[i]])
        args = judgment_color.missing_color(colors_name)
        Shortage_result = judgment_color.Shortage(args)

        #resultをソートして別々のリストに取り出す
        result.sort(key=lambda x: x[1], reverse=True)

        # resultリストを加工
        result ,color_graph =judgment_color.color_result_color(result)
        
        colors_code = [item[0] for item in result]
        colors_per = [item[1] for item in result]
        colors_name = [item[2] for item in result]
        # 色の点数表示
        inc_score_result = judgment_color.scoring_inc(result)
        color_score_inc = inc_score_result[0]
        nakai_color_zen = inc_score_result[1]
        color_point = inc_score_result[2] #色の点数
        color_point_name_code = inc_score_result[3] #色の点数の名前
        color_point_name_jp = inc_score_result[4] #色の点数の日本語名

        #全てまとめる
        all_result = [color_point,color_point_name_code,color_point_name_jp,colors_code,colors_per,color_graph,nakai_color_zen,gemini_response,Shortage_result]
        # リストをJSON形式の文字列に変換
        #これがないと保存できない（文字数の関係）
        all_result_str = json.dumps(all_result)

        # ユーザーIDを取得
        # ユーザーIDが取得できない（非ログイン時）場合は1を設定
        user_id = session.get('user_id', 2)

        try:
            sql = 'INSERT INTO lunch_score (user_id, score, lunch_image_name, use_gemini, is_not_lunch,all_result) VALUES (%s, %s, %s, %s, %s, %s)'
            mysql.cur.execute(sql, (user_id, color_score_inc, image_name, use_gemini_flag, is_not_lunch_flag,all_result_str))
            mysql.conn.commit()
            lunch_id = mysql.cur.lastrowid
        except Exception as e:
            if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                return
            else:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
        
        return render_template('image_result.html', response=gemini_response, colors_code=colors_code, colors_per=colors_per, colors_name=colors_name, Shortage_result=Shortage_result, data_uri=data_uri, color_score_inc=color_score_inc, nakai_color_zen=nakai_color_zen,color_graph=color_graph,color_point=color_point,color_point_name_code=color_point_name_code,color_point_name_jp=color_point_name_jp,id=lunch_id)   
    else:
        return redirect('/')
    
def gemini(image):
        prompt = variable.prompt
    
        # APIキーを設定
        genai.configure(api_key=API_KEY)

        # モデルの設定(画像の場合はgemini-1.5-flashを使用)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # 画像を読み込む
        picture_data = image.read()
        picture = [{
            # 画像のMIMEタイプ
            'mime_type': 'image/jpeg',
            # 画像をファイルパス(app.pyからの相対パス)から取得し、バイナリデータにする
            'data': picture_data
        }]

        response = model.generate_content(
            contents=[prompt, picture[0]]
        )
        return response.text
    
def colors_arg(image):
    colors, image_name = judgment_color.extract_dominant_colors_dbscan(image)

    colors_list = []
    for color_code, ratio in colors:
        # RGB値を16進数形式に変換
        hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
        colors_list.append([hex_color, ratio])

    judged_colors_list = judgment_color.judge_color(colors_list)
    
    return colors_list, judged_colors_list, image_name