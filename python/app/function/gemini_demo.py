import os
import base64
import traceback
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for
import google.generativeai as genai
from function import variable, easter_egg

app = Blueprint("gemini_demo", __name__)

API_KEY = os.getenv('gemini_api_key')

# テキストのみで会話をする場合の処理
@app.route('/gemini', methods=['GET', 'POST'])
def gemini():
    if request.method == 'POST':
        try:
            prompt = request.form['question']
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
        except Exception as e:
            tb = traceback.format_exc()
            tb.replace('\n', '<br>')
            easter_egg.cowsay(str(e), str(tb))
        else:
            return response.text + '<br><a href="/gemini">もう一度質問する</a>'
    else:
        return render_template('demo.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

# 画像から何かしらの質問をする場合の処理
@app.route('/gemini/image' , methods=['GET', 'POST'])
def gemini_image():
    if request.method == 'POST':
        prompt = variable.prompt
        image = request.files['image']
    
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

        # 画像をbase64にエンコード
        encoded_image = base64.b64encode(picture_data).decode('utf-8')
        # 画像をdataURIに変換
        data_uri = f"data:image/jpeg;base64,{encoded_image}"

        return render_template('image_result.html', response=response.text, image=data_uri)        
    else:
        return render_template('image.html')