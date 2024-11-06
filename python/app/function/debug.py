# -*- coding: utf-8 -*-

# デバック用いろいろ
from flask import Blueprint, render_template, request, redirect
from function import mysql
import os

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    sql = 'SELECT * FROM test'
    try:
        mysql.cur.execute(sql)
        result = mysql.cur.fetchall()
    except Exception as e:
        return str(e)
    return result

@app.route('/debug/mysql' , methods=['GET', 'POST'])
def debug_mysql():
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        try:
            sql = f"INSERT INTO test (name, value) VALUES ({name}, {value})"
            mysql.cur.execute(sql)
            mysql.conn.commit()
        except Exception as e:
            return str(e)
        return redirect('/debug/mysql')
    else:
        result = blueprint()
        return render_template('debug_mysql.html', result=result)
    
@app.route('/debug/processimagelist')
def processimagelist():
    image_dir = './static/images/rembg'
    image_files = []

    for filename in os.listdir(image_dir):
        if filename.endswith('.jpeg') or filename.endswith('.png'):
            image_files.append(filename)

    return {'images': image_files}