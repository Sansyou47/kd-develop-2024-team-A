import os
import base64
import concurrent.futures
import datetime
import json
import csv
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, make_response, session
import google.generativeai as genai
from function import variable, judgment_color, mysql
import os, json, requests
from datetime import datetime

app = Blueprint("gemini_demo", __name__)

app.register_blueprint(judgment_color.app)

API_KEY = os.getenv('gemini_api_key')
API_GATEWAY_ENDPOINT = os.getenv('API_GATEWAY_ENDPOINT')

@app.route('/intro')
def intro():
    return redirect('/')

# 画像を入力する画面に行くためのCookieなどの処理
@app.route('/takepic', methods=['GET', 'POST'])
def takepic():
    if request.method == 'POST':
        #有効時間（秒）
        age = 24 * 60 * 60
        expires = int(datetime.now().timestamp()) + age

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
        # grading_mode = 'selected_mode' in request.form
        grading_mode = 1
        if use_gemini:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                try:
                    future_response = executor.submit(gemini, image)  # gemini関数の実行
                    # 画像をクラスタリングし、色の名前をラベル付けまで行う
                    future_colors = executor.submit(new_colors_arg, image, grading_mode)  # colors_arg関数の実行
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
                    
                colors_list, colors_label_list, image_name = future_colors.result()  # colors_arg関数の結果を取得
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 画像をクラスタリングし、色の名前をラベル付けまで行う
                future_colors = executor.submit(new_colors_arg, image, grading_mode)  # colors_arg関数の実行
                use_gemini_flag = False
                is_not_lunch_flag = False
                
                colors_list, colors_label_list, image_name = future_colors.result()  # colors_arg関数の結果を取得
                gemini_response = None

        colors_code = [item[0] for item in colors_list]
        colors_per = [float(item[1]) for item in colors_list]
        result = []
        for i in range(len(colors_label_list)):
            result.append([colors_code[i], colors_per[i], colors_label_list[i]])
        Shortage_result = judgment_color.Shortage(judgment_color.missing_color(colors_label_list))

        #resultをソートして別々のリストに取り出す
        result.sort(key=lambda x: x[1], reverse=True)

        # resultリストを加工
        result ,color_graph =judgment_color.color_result_color(result)
        
        colors_code = [item[0] for item in result]
        colors_per = [item[1] for item in result]
        colors_name = [item[2] for item in result]
        # 色の点数表示
        inc_score_result = judgment_color.new_scoring_inc(result, grading_mode)
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
        csv_path = "./static/csv/iroiro.csv" #csvファイルのパス
        # color_perをcsvに書き込む
        with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(color_graph)
            writer.writerow(colors_per)

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

# リファクタリング後の関数（無駄なカラーコードの変換を削除、関数呼び出し回数の減少、変数の最適化など）
def new_colors_arg(image, grading_mode):
    # 採点モードの選択
    if grading_mode == 0:   # 簡単採点
        colors, image_name = judgment_color.extract_dominant_colors(image)

        colors_list = []
        for color_code, ratio in colors:
            # RGB値を16進数形式に変換
            hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
            colors_list.append([hex_color, ratio])

        judged_colors_list = judgment_color.judge_color(colors_list)
        
        return colors_list, judged_colors_list, image_name
    
    elif grading_mode == 1: # 高精度採点
        colors, image_name = judgment_color.extract_dominant_colors_dbscan(image)

        closest_colors_list = []    # hexカラーコードとその色名ラベルのリスト
        colors_per_list = []        # hexカラーコードと割合のリスト
        rgb_colors_list = []
        
        for color_code, ratio in colors:
            # RGBカラーコートをHSL色空間に変換
            hsl_color = judgment_color.rgb_to_hsl(color_code)
            # RGBをHEXカラーコードに変換
            hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
            
            rgb_colors_list.append(color_code)
            
            # カラーコードから色のラベリング
            # closest_color = judgment_color.find_closest_color_hsl(hsl_color)
            # 結果を変数に格納
            # closest_colors_list.append((hex_color, closest_color))
            colors_per_list.append([hex_color, ratio])
            
        hexAndLabelList = send_colorlist_to_lambda(rgb_colors_list)
    
        return colors_per_list, hexAndLabelList, image_name
    
def send_colorlist_to_lambda(text):
    # テキストデータをJSON形式に変換
    text = json.dumps(text)
    # ヘッダーの設定 (必要に応じて変更)
    headers = {
        'Content-Type': 'application/json'
    }

    # POSTリクエストを送信
    response = requests.post(API_GATEWAY_ENDPOINT, data=text, headers=headers)
    nowtime = datetime.now().strftime('%Y-%M-%D %H:%M:%S')

    # レスポンスのステータスコードをチェック
    if response.status_code == 200:
        print(f'aws lambda - - [{nowtime}] "info : color-labeling success" {response.status_code} -')   # 終了ステータスを標準入出力で書き出す
        # レスポンスの処理 (必要に応じて)
        result = response.json()    # 戻り値はカラーコードと色のラベル
        return result
    else:
        print(f'lambda - - [{nowtime}] "warning :" {response.status_code} color-labeling failed')   # 処理に失敗した際のメッセージ