from flask import Blueprint, render_template, request, redirect
from PIL import Image
import requests, os, io
from function import variable

app = Blueprint('remove_background', __name__)

REMBG_CONTAINER_NAME = os.getenv('REMBG_CONTAINER_NAME')
REMBG_CONTAINER_PORT = os.getenv('REMBG_CONTAINER_PORT')

# タイムアウト時間(秒)
timeout_value = 10

@app.route('/rembg')
def rembg_route():
    txt = process_image(variable.image_path)
    return txt

def process_image(image_path):
    try:
        image = Image.open(image_path)
    except IOError:
        return "画像を開けませんでした。"
    
    send_url = f"http://{REMBG_CONTAINER_NAME}:{REMBG_CONTAINER_PORT}/"
    
    byte_arr = io.BytesIO()
    image.save(byte_arr, format=image.format)
    byte_arr = byte_arr.getvalue()
    
    try:
        response = requests.post(send_url, files={'image': byte_arr}, timeout=timeout_value)
        response.raise_for_status()  # ステータスコードをチェック
    except requests.RequestException as e:
        return f"リクエスト中にエラーが発生しました: {e}"
    
    processed_image = Image.open(io.BytesIO(response.content))
    processed_image.save(variable.rembg_output_image_path)  # 出力画像を保存
    return response.text

def test():
    send_url = f"http://{REMBG_CONTAINER_NAME}:{REMBG_CONTAINER_PORT}/"
    response = requests.post(send_url, data="hogehoge")
    return response.text