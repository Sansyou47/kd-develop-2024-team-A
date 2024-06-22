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
    # color_codes = argment_color_output.extract_all_colors()
    colors = argment_color_output.extract_dominant_colors('./static/images/bento_01.jpg')
    argment_color_output.write_colors_to_csv(colors)
    # colors_list = variable.read_csv(variable.csv_path)
    # nc = argment_color_output.find_nearest_color()
    dominant_color_rgb = (0, 0, 0)  # 例としてのドミナントカラーのRGB値
    closest_color = argment_color_output.classify_color(dominant_color_rgb)
    return closest_color
    #return render_template('output_colors.html', colors_list=colors_list, nc = nc)

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")