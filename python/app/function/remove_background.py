from flask import Blueprint, render_template, request, redirect
from PIL import Image
import requests, os, io, time
from function import variable

app = Blueprint('remove_background', __name__)

# rembgコンテナのホスト名、ポート番号、プロセスキーを環境変数から取得
REMBG_CONTAINER_NAME = os.getenv('REMBG_CONTAINER_NAME')
REMBG_CONTAINER_PORT = os.getenv('REMBG_CONTAINER_PORT')
REMBG_PROCESSING_KEY = os.getenv('REMBG_PROCESSING_KEY')

# 画像処理のタイムアウト時間(秒)
# この時間を超えるとリクエストがタイムアウトする
timeout_value = 30

# デバッグ用ルーティングのため、本番では使用しない。
@app.route('/rembg', methods=['POST', 'GET'])
def rembg_route():
    if request.method == 'POST':
        image = request.files['image']
        image.save('./static/images/process_image.jpeg')
        txt = process_image()
        return txt
    else:
        return render_template('image_upload.html')

# 画像から背景を削除する処理を行う関数
# **************************************
# 引数: 画像ファイル
# 戻り値: 背景が削除された画像
# 画像処理に失敗した場合はエラーメッセージを返す
# **************************************
# この関数では、rembgコンテナに画像を送信し、背景が削除された画像を取得する。そのため、この関数内では画像の処理を行っていない。
# 画像処理を行うrembgコンテナへPOSTメソッドでプロセスキーを送信し、背景が削除された画像を取得する。
# 本来ならPOSTメソッドで画像ファイルを直接送信するが、エラーの修正ができなかったのでサーバーのディレクトリへ保存してからプロセスキーを送信してイベントを発火させる。
# プロセスキーを使用するのは、不正な操作でrembgの処理を時効されてしまうのを防ぐため、仕様上POSTで送信されると誰でも実行できてしまうため。
def process_image(image):
    # imageがPIL.Image.Image型のインスタンスであるかチェック
    if not isinstance(image, Image.Image):
    # imageがファイルパスまたはファイルライクオブジェクトであれば開く
        image = Image.open(image)
    # RGBAモードの画像をRGBモードに変換する
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    now = str(time.time())
    filename = f'process_image_{now}'
    image.save(f'./static/images/{filename}.jpeg')
    send_url = f"http://{REMBG_CONTAINER_NAME}:{REMBG_CONTAINER_PORT}/"
    data = {
        'processing_key': REMBG_PROCESSING_KEY,
        'filename': filename
    }
    response = requests.post(send_url, json=data, timeout=timeout_value)
    if response.status_code != 200:
        return 'Error: ' + response.text
    else:
        rembg_image = Image.open(f'./static/images/{filename}.png')
        return rembg_image