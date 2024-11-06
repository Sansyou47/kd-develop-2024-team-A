# -*- coding: utf-8 -*-

import pymysql, os, time
from pymysql.cursors import DictCursor

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# 接続試行回数の上限値
max_attempt = 10
interval = 10

def connect_to_mysql():
    for attempt in range(max_attempt):
        try:
            
            connection =pymysql.connect(
                host='mysql',
                port=int(3306),
                db=MYSQL_DATABASE,
                user=MYSQL_USER,
                passwd=MYSQL_PASSWORD,
                charset='utf8mb4',
                use_unicode=True
            )
            print("MySQLへの接続に成功しました。")

            return connection
        except pymysql.err.OperationalError as e:
            print(f"MySQLへの接続に失敗しました。{interval}秒後に再試行します。{e}")
            time.sleep(interval)
    print(f"MySQLへの接続に{max_attempt}回失敗しました。接続を中止します。")
    return None



connection = connect_to_mysql()

def init_db(conn):
    # connオブジェクトを関数の引数として受け取る
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET NAMES utf8mb4")
            cursor.execute("ALTER DATABASE kda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute("ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("文字コード設定に成功しました。")
        conn.commit()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()
        print("データベース接続を閉じました。")



init_db(connection)

# if __name__ == '__main__':
#     # 初期設定として一度だけ実行
#     init_db()
#     app.run(debug=True)
# if conn:
#     cur = conn.cursor()