from flask import Blueprint, render_template
# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("references", __name__)

@app.route('/references')
def references():
    return render_template("references.html")