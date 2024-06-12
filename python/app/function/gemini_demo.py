import os
import requests
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for
# Import the Python SDK with an alias
import google.generativeai as genai

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

# 画像から何かしらの質問をする場合の処理
@app.route('/gemini/image')
def gemini_image():
    # APIキーを設定
    genai.configure(api_key=API_KEY)

    # モデルの設定(画像の場合はgemini-pro-visionを使用)
    model = genai.GenerativeModel('gemini-pro-vision')

    # 画像を読み込む
    picture = [{
        # 画像のMIMEタイプ
        'mime_type': 'image/jpeg',
        # 画像をファイルパス(app.pyからの相対パス)から取得し、バイナリデータにする
        'data': Path('function/images/image.jpg').read_bytes()
    }]
    # 画像に関する質問を入力
    prompt = "この画像には何が写っていますか？:"

    response = model.generate_content(
        contents=[prompt, picture[0]]
    )
    return response.text