from flask import Blueprint

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("blueprint_demo", __name__)

@app.route('/blueprint')
def blueprint():
    return "Hello, Blueprint!"