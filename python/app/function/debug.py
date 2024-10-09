# デバック用いろいろ
from flask import Blueprint, render_template, request
from function import mysql

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    sql = 'SELECT * FROM test'
    mysql.cur.execute(sql)
    result = mysql.cur.fetchall()
    return str(result)

@app.route('/debug/mysql' , methods=['GET', 'POST'])
def debug_mysql():
    if request.method == 'POST':
        name = request.form.get('name') 
        value = request.form.get('value')
        mysql.cur.execute('INSERT INTO test (name, value) VALUES (%s, %s)', (name, value))
        mysql.conn.commit()
        return "ok"
    else:
        return render_template('debug_mysql.html')