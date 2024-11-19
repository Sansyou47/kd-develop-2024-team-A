from flask import Flask, render_template, request
from function import gemini_demo, judgment_color, Shortage, remove_background, debug, image_show, mypage, signup, ranking, tips, guide, x, login
from secrets import token_hex
import os

app = Flask(__name__)

# セッション情報を暗号化するためのキーを設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_HTTPONLY'] = True

# 分割したBlueprintのファイルから読み込む（ファイル名の後ろは拡張子ではないことに注意）
app.register_blueprint(gemini_demo.app)
app.register_blueprint(judgment_color.app)
app.register_blueprint(Shortage.app)
app.register_blueprint(remove_background.app)
app.register_blueprint(image_show.app) #サムネの画像表示用
app.register_blueprint(debug.app) #デバック用
app.register_blueprint(signup.app)
app.register_blueprint(mypage.app)
app.register_blueprint(ranking.app)
app.register_blueprint(tips.app)
app.register_blueprint(guide.app)
app.register_blueprint(login.app)
app.register_blueprint(x.app)

#session用の秘密鍵
# app.secret_key = token_hex(128)

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