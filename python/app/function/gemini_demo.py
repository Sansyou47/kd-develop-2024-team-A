import os
import base64
import requests
import concurrent.futures
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for
import google.generativeai as genai
from function import variable, judgment_color

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
        # モデルの設定(テキストの場合はgemini-proを使用)
        model = genai.GenerativeModel('gemini-pro')

        # 質問文を入力
        response = model.generate_content(prompt)
        return response.text + '<br><a href="/gemini">もう一度質問する</a>'
    else:
        return render_template('gemini.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

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
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_response = executor.submit(gemini, image)  # gemini関数の実行
            future_colors = executor.submit(colors_arg, image)  # colors_arg関数の実行
            
            response = future_response.result()  # gemini関数の結果を取得
            colors_list, judged_colors_list = future_colors.result()  # colors_arg関数の結果を取得

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
        result =judgment_color. color_result_color(result)
        
        colors_code = [item[0] for item in result]
        colors_per = [item[1] for item in result]
        colors_name = [item[2] for item in result]

        return render_template('result.html', response=response, colors_code=colors_code, colors_per=colors_per, colors_name=colors_name, Shortage_result=Shortage_result, data_uri=data_uri)        
    else:
        return render_template('image.html')
    
def gemini(image):
        prompt = variable.prompt
    
        # APIキーを設定
        genai.configure(api_key=API_KEY)

        # モデルの設定(画像の場合はgemini-pro-visionを使用)
        model = genai.GenerativeModel('gemini-pro-vision')
        
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
    colors = judgment_color.extract_dominant_colors(image)

    judgment_color.write_colors_to_csv(colors)

    colors_list = []
    for color_code, ratio in colors:
        # RGB値を16進数形式に変換
        hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
        colors_list.append([hex_color, ratio])

    judged_colors_list = judgment_color.judge_color(colors_list)
    
    return colors_list, judged_colors_list