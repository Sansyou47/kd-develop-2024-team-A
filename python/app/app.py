from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image
# 分割したファイルを読み込む。ディレクトリはfunctionディレクトリからの相対パスを指定している。
from function import blueprint_demo, gemini_demo, easter_egg, judgment_color, Shortage, remove_background, debug

app = Flask(__name__)

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(blueprint_demo.app)
app.register_blueprint(gemini_demo.app)
app.register_blueprint(easter_egg.app)
app.register_blueprint(judgment_color.app)
app.register_blueprint(Shortage.app)
app.register_blueprint(remove_background.app)
app.register_blueprint(debug.app)

# インデックスルート
@app.route('/')
def index():
    #クッキーから情報を取得
    access = request.cookies.get('access')
    
    #クッキーが無ければaccessにfalseを代入
    if access != 'true':
        access = 'false'
    
    #intro.htmlにaccessを渡す
    return render_template('intro.html', access=access)

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")