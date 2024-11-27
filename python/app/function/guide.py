from flask import Blueprint, render_template

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("guide", __name__)

@app.route('/guide')
def guide():
    return render_template("guide.html")