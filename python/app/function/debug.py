# デバック用いろいろ
from flask import Blueprint, render_template, request, redirect, session
from function import mysql
import os, json

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("debug", __name__)

@app.route('/debug')
def blueprint():
    if "user_id" in session:
        uid = session["user_id"]
        if uid == 1:
            sql = 'SELECT * FROM test'
            try:
                mysql.cur.execute(sql)
                result = mysql.cur.fetchall()
            except Exception as e:
                return str(e)
            return result
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/debug/mysql' , methods=['GET', 'POST'])
def debug_mysql():
    if "user_id" in session:
        uid = session["user_id"]
        if uid == 1:
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
        else:
            return redirect('/login')
    else:
        return redirect('/login')
    
@app.route('/debug/processimagelist')
def processimagelist():
    if "user_id" in session:
        uid = session["user_id"]
        if uid == 1:
            image_dir = './static/images/process'
            image_files = []

            for filename in os.listdir(image_dir):
                if filename.endswith('.jpeg') or filename.endswith('.png'):
                    image_files.append(filename)

            return {'images': image_files}
        else:
            return redirect('/login')
        
@app.route('/debug/scoreresult')
def scoreresult():
    if "user_id" in session:
        uid = session["user_id"]
        if uid == 1:
            sql ='SELECT all_result FROM lunch_score WHERE user_id = 1'
            try:
                mysql.cur.execute(sql)
                result = mysql.cur.fetchall()
            except Exception as e:
                return str(e)
            
            result = json.loads(result[0][0])
            return str(result)
        else:
            return redirect('/login')
    else:
        return redirect('/login')