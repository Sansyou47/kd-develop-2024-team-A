from flask import Blueprint, jsonify
import csv

#このページでやること
#tipsを予めcsvに書き込んでおき、それを読み込んで表示する

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("tips", __name__)
@app.route('/tips', methods=['GET', 'POST'])
#scvファイルを読み込む関数
def tips_csv():
    tips_list = [] #tipsのリスト
    csv_path = "./static/csv/tips.csv" #csvファイルのパス
    with open(csv_path, mode='r', encoding = "utf-8",newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            tips_list.append(row[0])
    return jsonify(tips_list) #tipsのリストをjson形式で返す