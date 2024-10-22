import os
import base64
import requests
import concurrent.futures
import datetime
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, make_response, session
import google.generativeai as genai
from function import variable, judgment_color, mysql

app = Blueprint("gemini_demo", __name__)

app.register_blueprint(judgment_color.app)

API_KEY = os.getenv('gemini_api_key')

# テキストのみで会話をする場合の処理
@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    if request.method == 'POST':
        prompt = request.form['question']
        # APIキーを設定
        genai.configure(api_key=API_KEY)
        # モデルの設定(テキストの場合はgemini-1.5-flashを使用)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 質問文を入力
        response = model.generate_content(prompt)
        return response.text + '<br><a href="/gemini">もう一度質問する</a>'
    else:
        return render_template('gemini.html')

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
                future_response = executor.submit(gemini, image)  # gemini関数の実行
                future_colors = executor.submit(colors_arg, image)  # colors_arg関数の実行
                
                try:
                    response = future_response.result()  # gemini関数の結果を取得
                except Exception as e:
                    response = None
                    title = 'Oops！エラーが発生しちゃった！😭'
                    message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                    return render_template('error.html', title=title, message=message, error=e)
                    
                colors_list, judged_colors_list, image_name = future_colors.result()  # colors_arg関数の結果を取得
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # future_response = executor.submit(gemini, image)  # gemini関数の実行
                future_colors = executor.submit(colors_arg, image)  # colors_arg関数の実行
                
                # response = future_response.result()  # gemini関数の結果を取得
                colors_list, judged_colors_list, image_name = future_colors.result()  # colors_arg関数の結果を取得

                response = None

        # return 'judged_colors_list=' + str(judged_colors_list) + '<br>' + 'colors_list=' + str(colors_list)
        colors_code = [item[0] for item in colors_list]
        colors_per = [float(item[1]) for item in colors_list]
        colors_name = [item[1] for item in judged_colors_list]
        result = []
        for i in range(len(judged_colors_list)):
            result.append([colors_code[i], colors_per[i], colors_name[i]])
        Shortage_result = judgment_color.Shortage(judgment_color.missing_color(colors_name))

        #resultをソートして別々のリストに取り出す
        result.sort(key=lambda x: x[1], reverse=True)
        # colors_code = [item[0] for item in result]
        # colors_per = [item[1] for item in result]
        # colors_name = [item[2] for item in result]

        # resultリストを加工
        result ,color_graph =judgment_color. color_result_color(result)
        
        colors_code = [item[0] for item in result]
        colors_per = [item[1] for item in result]
        colors_name = [item[2] for item in result]
        # 色の点数表示
        color_score_dec = judgment_color.scoring_dec(result)
        inc_socre_result = judgment_color.scoring_inc(result)
        color_score_inc = inc_socre_result[0]
        token_point = inc_socre_result[1]
        reason = inc_socre_result[2]
        nakai_color_zen = inc_socre_result[3]
        
        # ユーザーIDを取得
        # ユーザーIDが取得できない（非ログイン時）場合は1を設定
        user_id = session.get('user_id', 1)
        
        try:
            sql = 'INSERT INTO lunch_score (user_id, score, lunch_image_name) VALUES (%s, %s, %s)'
            mysql.cur.execute(sql, (user_id, color_score_inc, image_name))
            mysql.conn.commit()
        except Exception as e:
            title = 'Oops！エラーが発生しちゃった！😭'
            message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
            return render_template('error.html', title=title, message=message, error=e)
        
        # Geminiを使用するにチェックボックスが入っている場合はresponse=responseを行い
        # そうでない場合はresponse=responseを行わない
        return render_template('image_result.html', response=response, colors_code=colors_code, colors_per=colors_per, colors_name=colors_name, Shortage_result=Shortage_result, data_uri=data_uri, color_score_inc=color_score_inc,color_score_dec=color_score_dec,token_point=token_point,reason=reason, nakai_color_zen=nakai_color_zen,color_graph=color_graph)   
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
    colors, image_name = judgment_color.extract_dominant_colors(image)

    judgment_color.write_colors_to_csv(colors)

    colors_list = []
    for color_code, ratio in colors:
        # RGB値を16進数形式に変換
        hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
        colors_list.append([hex_color, ratio])

    judged_colors_list = judgment_color.judge_color(colors_list)
    
    return colors_list, judged_colors_list, image_name