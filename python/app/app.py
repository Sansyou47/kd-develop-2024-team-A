from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image
# 分割したファイルを読み込む。ディレクトリはfunctionディレクトリからの相対パスを指定している。
from function import pil_demo, blueprint_demo, gemini_demo, easter_egg, argment_color_output, variable
import subprocess, re

app = Flask(__name__)

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(blueprint_demo.app)
app.register_blueprint(gemini_demo.app)
app.register_blueprint(easter_egg.app)

# インデックスルート
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pil')
def pil():
    image = 'syub.jpg'
    colors = argment_color_output.extract_dominant_colors('./static/images/' + image)
    argment_color_output.write_colors_to_csv(colors)
    colors_list = variable.read_csv(variable.csv_path)
    colors_code = [item[0] for item in colors_list]
    colors_per = [item[1] for item in colors_list]
    colors_list = argment_color_output.judge_color_from_csv(variable.csv_path)
    
    #return '変数名：colors_list：' + str(colors_list) + '<br>変数名：colors_code：' + str(colors_code) + '<br>変数名：colors_per：' + str(colors_per)

    return render_template('output_colors.html', colors_list=colors_list, colors_code=colors_code, colors_per=colors_per, img = '../static/images/' + image)

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")