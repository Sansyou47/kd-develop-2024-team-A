import pymysql, os, time

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# 接続試行回数の上限値
max_attempt = 5
interval = 5

def connect_to_mysql():
    for attempt in range(max_attempt):
        try:
            conn = pymysql.connect(
                host='mysql',
                port=int(3306),
                db=MYSQL_DATABASE,
                user=MYSQL_USER,
                passwd=MYSQL_PASSWORD,
                charset='utf8',
            )
            print("MySQLへの接続に成功しました。")
            return conn
        except pymysql.err.OperationalError as e:
            print(f"MySQLへの接続に失敗しました。{interval}秒後に再試行します。{e}")
            time.sleep(interval)
    print(f"MySQLへの接続に{max_attempt}回失敗しました。接続を中止します。")
    return None

conn = connect_to_mysql()
if conn:
    cur = conn.cursor()