from flask import Blueprint, render_template, request, redirect
from PIL import Image
import requests, os, io
from function import variable

app = Blueprint('remove_background', __name__)

REMBG_CONTAINER_URL = os.getenv('REMBG_CONTAINER_URL')
REMBG_CONTAINER_PORT = os.getenv('REMBG_CONTAINER_PORT')

@app.route('/rembg')
def rembg_route():
    process_image(variable.image_path)
    return '背景を除去しました'
    
def rembg(input_path, output_path):
    input = Image.open(input_path) # 入力画像を開く
    # output = remove(input)         # 背景を除去
    # output.save(output_path)       # 出力画像を保存

def process_image(image_data):
    # 画像データがバイト列の場合、io.BytesIOを使用してファイルライクオブジェクトに変換
    # if isinstance(image_data, bytes):
    #     image_data = io.BytesIO(image_data)
    
    image = Image.open(image_data)  # 修正: バイト列をファイルライクオブジェクトに変換してから開く
    
    send_url = f"{REMBG_CONTAINER_URL}:{REMBG_CONTAINER_PORT}/ImageProcessor"
    
    byte_arr = io.BytesIO()
    image.save(byte_arr, format=image.format)
    byte_arr = byte_arr.getvalue()
    
    response = requests.post(send_url, files={'image': byte_arr})
    processed_image = Image.open(io.BytesIO(response.content))
    
    processed_image.save(variable.output_image_path)  # 出力画像を保存