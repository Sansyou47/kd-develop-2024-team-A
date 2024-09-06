from flask import Blueprint
import random
from function import variable

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("Shortage", __name__)

@app.route('/Shortage')
def Shortage():
    missing_color = ['blue','pink','purple','orange','yellow','green','red']

    missing_vegetables = variable.missing_vegetables

    
    missing = []

    # 各色ごとに処理を行う
    for color in missing_color:
        # 色が一致する野菜を抽出
        filtered_vegetables = []
        # missing_vegetablesの各要素について処理
        for veg in missing_vegetables:
            # 野菜の色が指定された色と一致するかを確認
            if veg[1] == color:
                # 一致する場合、その野菜をfiltered_vegetablesに追加
                filtered_vegetables.append(veg[0])
        
        # ランダムに選ぶ数を決定（最大2つ、filtered_vegetablesの長さ以下）
        num_to_select = min(2, len(filtered_vegetables))
        # 抽出した野菜の中からランダムにnum_to_select個を選ぶ
        selected_vegetables = random.sample(filtered_vegetables, num_to_select)
        # 選んだ野菜を不足リストに追加
        missing.extend(selected_vegetables)

    # 結果を返す
    return str(missing) + 'が不足しています。'