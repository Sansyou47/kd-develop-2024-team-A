from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image
# 分割したファイルを読み込む。ディレクトリはfunctionディレクトリからの相対パスを指定している。
from function import pil_demo, blueprint_demo, gemini_demo, easter_egg, argment_color_output, variable, Shortage
import subprocess, re, base64

app = Flask(__name__)

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(blueprint_demo.app)
app.register_blueprint(gemini_demo.app)
app.register_blueprint(easter_egg.app)
app.register_blueprint(Shortage.app)

# インデックスルート
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/colors', methods=['GET', 'POST'])
def pil():
    if request.method == 'POST':
        image = request.files['image']
        colors = argment_color_output.extract_dominant_colors(image)
        argment_color_output.write_colors_to_csv(colors)
        colors_list = variable.read_csv(variable.csv_path)
        sorted_colors_list = sorted(colors_list,key=lambda x: float(x[1]), reverse=True) #割合の多い順に並べ替え
        colors_code = [item[0] for item in sorted_colors_list]
        colors_per = [item[1] for item in sorted_colors_list]
        colors_list = argment_color_output.judge_color_from_csv(variable.csv_path)
        colors_name = [item[1] for item in colors_list]

        content_type = ''
        # ファイル形式を取得
        if 'png' in image.content_type:
            content_type = 'png'
        elif 'jpg' in image.content_type:
            content_type = 'jpg'

        # bytesファイルのデータをbase64にエンコードする
        uploadimage_base64 = base64.b64encode(image.stream.read())
        
        # base64形式のデータを文字列に変換する。その際に、「b'」と「'」の文字列を除去する
        uploadimage_base64_string = re.sub('b\'|\'', '', str(uploadimage_base64))
        
        # 「data:image/png;base64,xxxxx」の形式にする
        filebinary = f'data:image/{content_type};base64,{uploadimage_base64_string}'
        
        #return '変数名：colors_list：' + str(colors_list) + '<br>変数名：colors_code：' + str(colors_code) + '<br>変数名：colors_per：' + str(colors_per)

        return render_template('output_colors.html', colors_list=colors_list, colors_code=colors_code, colors_per=colors_per, colors_name=colors_name, sorted_colors_list=sorted_colors_list, image=filebinary)
    else:
        return render_template('judge_color.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")