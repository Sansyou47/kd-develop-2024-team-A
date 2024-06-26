import os
import base64
import requests
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for
# Import the Python SDK with an alias
import google.generativeai as genai
from function import variable

app = Blueprint("gemini_demo", __name__)

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

        return render_template('result.html', response=response.text, image=data_uri)        
    else:
        return render_template('image.html')