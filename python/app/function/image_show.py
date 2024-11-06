# -*- coding: utf-8 -*-

from flask import Blueprint,render_template

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("image_show", __name__)

@app.route('/SnapScoreLogo')
def blueprint():
    return render_template('SnapScoreLogo.html')