from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image
# 分割したファイルを読み込む。ディレクトリはfunctionディレクトリからの相対パスを指定している。
from function import pil_demo, variable, blueprint_demo, gemini_demo
import subprocess, re

app = Flask(__name__)

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(blueprint_demo.app)
app.register_blueprint(gemini_demo.app)

# インデックスルート
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pil')
def pil():
    pil_demo.rrr()
    return "Hello, PIL!"

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/contact')
def contact():
    # cowsayコマンドを実行
    result = subprocess.run(['/usr/games/cowsay', '-f', 'dragon', 'コンタクトは取れないヨ！'], encoding='utf-8', stdout=subprocess.PIPE)
    # 連続する空白を&nbsp;に置換
    formatted_text = re.sub(r' {2,}', lambda match: '&nbsp;' * len(match.group()), result.stdout)
    # 改行を<br>タグに置換
    formatted_text = formatted_text.replace('\n', '<br>')
    # 置換したテキストをHTMLに渡す
    return render_template('out.html', text=formatted_text)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")