# デバック用いろいろ

from flask import Blueprint, render_template
from function import mysql

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    sql = 'SELECT * FROM test'
    mysql.cur.execute(sql)
    result = mysql.cur.fetchall()
    return str(result)