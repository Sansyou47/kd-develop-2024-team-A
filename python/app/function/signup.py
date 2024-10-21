from flask import Blueprint, render_template, request, redirect, url_for
from function import mysql
from werkzeug.security import generate_password_hash

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("signup", __name__)
# 昔の奴みようね
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        try:
            sql = 'INSERT INTO users (name, password, email) VALUES (%s, %s, %s)'
            mysql.cur.execute(sql, (name, hashed_password, email))
            mysql.conn.commit()
        except Exception as e:
            return str(e)
        return redirect(url_for('success'))
    return render_template('signup.html')

# ページ表示用のデバック
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)