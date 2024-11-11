from flask import Blueprint, render_template, request, redirect, session
from function import mysql
import os

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("x", __name__)
# color_score_inc=score,
# token_point=token_point, 
# data_uri=bento_url,
# color_point=color_point,
# color_point_name_code=color_point_name_code,
# color_point_name_jp=color_point_name_jp,
# colors_code=colors_code,
# colors_per=colors_per,
# color_graph=color_graph,
# nakai_color_zen=nakai_color_zen,
# response=gemini_response,
# Shortage_result=Shortage_result
# データベースからすべてのデータを取得して完了
@app.route('/x', methods=['GET', 'POST'])
def x():
    color_score_inc = None
    token_point = None
    data_uri = None
    color_point = None
    color_point_name_code = None
    color_point_name_jp = None
    colors_code = None
    colors_per = None
    color_graph = None
    nakai_color_zen = None
    response = None
    Shortage_result = None
# 文字数数えろ
    if request.method == 'POST':

    return render_template('image_result.html')