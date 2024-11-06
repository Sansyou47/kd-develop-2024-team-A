# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect
from rembg import remove
from PIL import Image
from function import variable

app = Blueprint('rembg_practice', __name__)

@app.route('/rembg')
def rembg():
    remove_background(variable.image_path, variable.output_image_path)
    return '背景を除去しました'
    
def remove_background(input_path, output_path):
    input = Image.open(input_path) # 入力画像を開く
    output = remove(input)         # 背景を除去
    output.save(output_path)       # 出力画像を保存