# デバック用いろいろ

from flask import Blueprint, render_template

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    return render_template('debug.html')