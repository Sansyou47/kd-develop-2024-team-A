# デバック用いろいろ
from flask import Blueprint, render_template
from function import mysql, hoge

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    sql = 'SELECT * FROM test'
    mysql.cur.execute(sql)
    result = mysql.cur.fetchall()
    return str(result)

# クラスのあれこれ
@app.route('/debug2')
def blueprint2():
    # クラスのインスタンス化
    prt = hoge.Test('井上', 20)
    # インスタンスのメソッドを呼び出す
    prt.__str__()
    return 'OK'

@app.route('/debug3')
def debug3():
    rgb = (255, 255, 0)
    hex = hoge.Rgb_to_Hex(rgb)
    return hex.rgb_to_hex()