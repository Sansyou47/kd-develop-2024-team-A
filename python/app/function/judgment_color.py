from flask import Blueprint, render_template, request
from PIL import Image
from function import variable, remove_background, mysql
from decimal import Decimal, ROUND_HALF_UP
import csv
import numpy as np
import colorsys
from sklearn.cluster import KMeans
import random

app = Blueprint('judgment_color', __name__)

def extract_all_colors():
    # 画像を読み込む
    with Image.open(variable.image_path) as img:
        # 画像のサイズを取得
        width, height = img.size
        # 色コードを格納するリスト
        color_codes = []
        # 画像の全ピクセルをループ処理
        for x in range(width):
            for y in range(height):
                # ピクセルの色（RGB）を取得
                color = img.getpixel((x, y))
                # RGB値を16進数の色コードに変換
                color_code = "#{:02x}{:02x}{:02x}".format(*color)
                # 色コードをリストに追加
                color_codes.append(color_code)
        return color_codes
    
# 色コードと割合のリストをCSVファイルに書き込む関数
def write_colors_to_csv(color_codes_with_ratios):
    csv_path=variable.csv_path
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # sorted_color_codes_with_ratios = sorted(color_codes_with_ratios, key=lambda x: x[1], reverse=True)
        for color_code, ratio in color_codes_with_ratios:
            # RGB値を16進数形式に変換
            hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
            # 色コードと割合を書き込む
            writer.writerow([hex_color, ratio])
        
# 画像からドミナントカラーを抽出する関数
# 第1引数：画像データ（PIL.Image）
# 第2引数：クラスタリングする色の数
# 戻り値：ドミナントカラーのRGB値と割合のリスト
def extract_dominant_colors(image, num_colors=150):
    up_to_saturation_ratio = 1.5
    # process_image関数へ画像を渡し、背景除去後の画像を取得
    removebg_image, image_name = remove_background.process_image(image)

    #画像がRGBでない場合、RGBに変換
    if removebg_image.mode != 'RGB':
        removebg_image = removebg_image.convert('RGB')
        
    # 彩度を上げるために画像をHSVに変換
    hsv_image = removebg_image.convert('HSV')
    hsv_array = np.array(hsv_image)
    
    # 彩度を上げる（例：1.5倍）
    hsv_array[..., 1] = np.clip(hsv_array[..., 1] * up_to_saturation_ratio, 0, 255)
    
    # HSVからRGBに戻す
    removebg_image = Image.fromarray(hsv_array, 'HSV').convert('RGB')
    
    # # 画像を保存
    # save_path = f'./rmbg/{image_name}_saturation={up_to_saturation_ratio}.png'
    # removebg_image.save(save_path)

    pixels = np.array(removebg_image).reshape(-1, 3)
    
    # 色コードが#000000のピクセルを除外
    pixels = pixels[~np.all(pixels == 0, axis=1)]
    
    # k-meansクラスタリングを実行
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # 各クラスタの中心点（ドミナントカラー）を取得
    dominant_colors = kmeans.cluster_centers_.astype(int)
    
    # 各ピクセルが属するクラスタのインデックスを取得
    labels = kmeans.labels_
    
    # 各ドミナントカラーの割合を計算
    color_counts = np.bincount(labels)
    total_pixels = len(labels)
    color_ratios = (color_counts / total_pixels) * 100
    color_ratios = color_ratios.round(2)
    
    # RGB値と割合のタプルのリストを返す
    return [(tuple(color), ratio) for color, ratio in zip(dominant_colors, color_ratios)], image_name

# 12色相環を定義
color_wheel_12 = ['red', 'orange', 'yellow',
               'yellow-green', 'green', 'lime-green',
               'light-blue', 'light-blue', 'blue',
               'purple', 'pink', 'red']

# 24色相環を定義
color_wheel_24 = ['red', 'vermilion', 'orange', 'amber', 'yellow', 'yellow-green',
               'green', 'spring-green', 'cyan', 'sky-blue', 'blue', 'ultramarine',
               'violet', 'purple', 'magenta', 'rose', 'crimson', 'raspberry',
               'burgundy', 'rust', 'tangerine', 'apricot', 'beige', 'peach']

scoring_color_inc = ['red', 'yellow','green', 'white', 'black', 'brown', 'blue', 'gray']

scoring_point_inc = [6, 28, 9, 10, 10, 20, 0, 10]

scoring_color_dec = ['green-blue', 'light-blue', 'blue','purple']

scoring_point_dec = [50]

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGBに変換"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsv(rgb_color):
    """RGBをHSVに変換"""
    return colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)

# HSVの色相、彩度、明度から最も近い色を判定する関数（閾値を弁当の写真用にチューニングしているため、弁当以外の画像には適用できない可能性があることに注意）
def find_closest_color(hsv_color):
    # HSV：Hue（色相）、Saturation（彩度）、Value（明度）
    hue, saturation, value = hsv_color
    hue *= 360  # 色相を度に変換
    # 白の閾値（色相の範囲、彩度、明度を指定）
    white_hue_range = (28, 72)
    white_saturation_threshold = 0.15
    white_value_threshold = 0.85
    # 灰色の閾値（彩度がこの値より小さい場合は灰色と判定）
    gray_saturation_threshold = 0.2
    # 黒の閾値（明度がこの値より小さい場合は黒と判定）
    black_threshold = 0.2
    # 茶色の判定基準
    brown_hue_range = (0, 50)
    brown_saturation_threshold = 0.3
    brown_value_range = (0.2, 0.7)

    # 白の判定
    if  white_hue_range[0] >= hue <= white_hue_range[1] and value > white_value_threshold and saturation < white_saturation_threshold:
        return 'white'
    # 黒の判定
    elif value < black_threshold:
        return 'black'
    # 灰色の判定
    elif saturation < gray_saturation_threshold:
        return 'gray'
    # 茶色の判定
    elif brown_hue_range[0] <= hue <= brown_hue_range[1] and saturation > brown_saturation_threshold and brown_value_range[0] <= value <= brown_value_range[1]: #or brown_hue_range[0] <= hue <= brown_hue_range[1]:
        return 'brown'
    else:
        # 12色相環の判定（30=360/12）
        index = int(Decimal(hue/30).to_integral_value(rounding=ROUND_HALF_UP)) % 12
        return color_wheel_12[index]

def judge_color_from_csv(csv_path):
    """CSVファイルから色を判定"""
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        closest_color_list = []
        for row in reader:
            hex_color = row[0]
            rgb_color = hex_to_rgb(hex_color)
            hsv_color = rgb_to_hsv(rgb_color)
            closest_color = find_closest_color(hsv_color)  # hsv_color全体を渡す
            closest_color_list.append((hex_color, closest_color))
        return closest_color_list
    
def judge_color(color_code):
    closest_color_list = []
    for row in color_code:
        hex_color = row[0]
        rgb_color = hex_to_rgb(hex_color)
        hsv_color = rgb_to_hsv(rgb_color)
        closest_color = find_closest_color(hsv_color)  # hsv_color全体を渡す
        closest_color_list.append((hex_color, closest_color))
    return closest_color_list

def Shortage(missing_color):

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
    #4つの不足食材を取得、4つ以下ならそのまま
    if len(missing) >= 4:
        missing = random.sample(missing, 4)

    # 結果を返す
    missing = '<br>'.join([veg for veg in missing if veg])
    return str(missing) + '<br>などを入れるとより良いお弁当になるかもしれません。'

def missing_color(colors_name):
    #missing_colorをShortage関数に渡す
    #足りていない色を抽出する
    # 12色相環を定義+白+黒灰+茶を定義
    # color_name[i]には色の名前が入っている
    color_list_15 = ['red', 'orange', 'yellow',
                'yellow-green', 'green', 'light-green',
                'green-blue', 'light-blue', 'blue',
                'purple', 'pink', 'white', 'black', 'gray', 'brown']
    missing_color = [color for color in color_list_15 if color not in colors_name]
    return missing_color

def color_result_color(result):
    result.sort(key=lambda x: x[1], reverse=True)
    color_per = {}
    color_code = {}
    result_color_per = []
    for item in result:
        name = item[2]
        per = item[1]
        code = item[0]
        if name in color_per:
            color_per[name] += per
        else:
            color_per[name] = per
            color_code[name] = code

    for name, per in color_per.items():
        per = round(per, 2)
        result_color_per.append([color_code[name], per, name])

    result_color_per.sort(key=lambda item: item[1], reverse=True)
    
    #色を日本語に変換
    color_names_jp = {
            'red': '赤',
            'orange': 'オレンジ',
            'yellow': '黄色',
            'yellow-green': '黄緑',
            'green': '緑',
            'light-green': 'ライトグリーン',
            'green-blue': '青緑',
            'light-blue': 'ライトブルー',
            'blue': '青',
            'purple': '紫',
            'pink': 'ピンク',
            'white': '白',
            'black': '黒',
            'gray': '灰色',
            'brown': '茶色'
        }
    # item2 配列の色を日本語に変換して color_grahp に保存
    color_graph = []
    for item in result_color_per:
        if isinstance(item[2], str):
            color_graph.append(color_names_jp.get(item[2], '不明'))
        elif isinstance(item[2], (list, tuple)):
            color_graph.extend([color_names_jp.get(color, '不明') for color in item[2]])
        else:
            color_graph.append('不明')

    return result_color_per,color_graph

def scoring_inc(result):
    #結果点数の初期化
    point_inc = 0

    #色の影響設定0.5は各色に値の*0.5して計算
    color_mappings = {
    # color_var weight
    'red': [('red', 1)],
    'orange': [('yellow', 1)],
    'yellow': [('yellow', 0.5), ('green', 0.5)],
    'yellow-green': [('green', 0.5)],
    'green': [('green', 1)],
    'light-green': [('green', 1)],
    'green-blue': [('green', 1)],
    'light-blue': [('blue', 1)],
    'blue': [('blue', 1)],
    'purple': [('black', 1)],
    'pink': [('red', 1)],
    'white': [('white', 1)],
    'black': [('black', 1)],
    'gray': [('gray', 0.5), ('white', 0.5)],
    'brown': [('brown', 1)],
}
    # 色の名前を日本語に変換するマッピング
    color_names_jp = {
        'red': '赤',
        'yellow': '黄',
        'green': '緑',
        'white': '白',
        'black': '黒',
        'brown': '茶',
        'gray': '灰'
    }

    # 色の名前をカラーコードに変換するマッピング
    color_names_code = {
        'red': '#ff0000',
        'yellow': '#ffff00',
        'green': '#008000',
        'white': '#ffffff',
        'black': '#000000',
        'brown': '#8c3608',
        'gray': '#808080'
    }

    # 各色 閾値 最大点 採点 パーセンテージ 棒グラフの点数
    #これが更新されreturnに返す
    colors_info = {
        'red': {'threshold': 10, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'yellow': {'threshold': 18, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'green': {'threshold': 12, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'white': {'threshold': 10, 'points': 10, 'score': 0,'per':0,'bar_point':0},
        'black': {'threshold': 17, 'points': 10, 'score': 0,'per':0,'bar_point':0},
        'brown': {'threshold': 16, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'gray': {'threshold': 10, 'points': 10, 'score': 0,'per':0,'bar_point':0},
    }
    
    for item in result:
        #各色と%取り出し
        per = item[1]
        name = item[2]
        if name in color_mappings:
            #mappingの左側の値をcolor_varに、右側の値をweightとして取り出す
            for color_var, weight in color_mappings[name]:
                # buleの場合は処理をスキップ
                if color_var == 'blue':
                    continue
                colors_info[color_var]['per'] += per * weight
    #最終的なパーセンテージ値を小数点2位まで丸める
    for color in colors_info:
        colors_info[color]['per'] = round(colors_info[color]['per'], 2)
        
    sub_comment = ''
    # 各色に対してループ
    #infoには色に対応する'threshold': , 'points': , 'score': ,'per':が含まれる
    #使う際にはinfo['threshold']などで取り出す
    for color, info in colors_info.items():
        #色の%と閾値を比較して点数を計算
        #閾値以上の場合は点数をそのまま返す
        if info['per'] >= info['threshold']:
            info['score'] = info['points']
            #棒グラフ計算
            info['bar_point'] = info['points']
            
        #以下は閾値未満の場合の計算
        #赤色の場合のみ特別な計算を行う
        elif color == 'red':
            info['score'] = max(info['points'] - int((info['threshold'] - info['per']) / 0.2), 0)
            # 棒グラフ計算
            proportion = info['per'] / info['threshold']
            info['bar_point'] = info['points'] * proportion
            
        # それ以外の色の場合の計算
        else:
            info['score'] = max(info['points'] - int((info['threshold'] - info['per']) / 0.4), 0)
            # 棒グラフ計算
            proportion = info['per'] / info['threshold']
            info['bar_point'] = info['points'] * proportion
        #点数を加算
        point_inc += info['score']
    
    if (colors_info['white']['per'] + colors_info['gray']['per']) >= 20:
        sub_comment = '白色が少し多いようです。白のような無彩色は食欲を増進させることができません。'

    #各色の点数を100点満点に変換
    for color, info in colors_info.items():
        #pointsが20点の場合、multipleは5
        multiple = 100 / info['points']
        #scoreをmultiple倍する
        info['bar_point'] *= multiple
        #scoreを整数に変換
        info['bar_point'] = int(info['bar_point'])
    
    nakai_perfect_zen = []
    
    perfect_comment = ''
    shortage_comment = ''
    bad_score = 100
    # 赤、緑、黄のそれぞれが100点なら1点追加、3点満点で彩が完璧だとメッセージを送る目的の変数
    RGY_perfect = 0
    
    color_point = [] #色の点数
    color_point_name_code = [] #色の点数のカラーコード
    color_point_name_jp = [] #色の点数の日本語名

    # 各色に対する評価コメントの追加処理
    for color, info in colors_info.items():
        #色の表示
        color_point.append(info["bar_point"])
        color_point_name_code.append(color_names_code[color])
        color_point_name_jp.append(color_names_jp[color])
        
        # 個別の色のスコアが満点だった場合
        if info['score'] == info['points']:
            try:
                # DBから対応する色の肯定的なコメントを取得する
                sql = 'SELECT comment FROM lunch_comment WHERE color = %s AND is_positive = TRUE ORDER BY RAND() LIMIT 1'
                mysql.cur.execute(sql, (color,))
                comment = mysql.cur.fetchone()
                
            except Exception as e:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
                
            # 対応する色のコメントが存在しなかった場合
            if comment is not None:
                comment = str(comment[0])
                nakai_perfect_zen.append(comment)
                # perfect_comment = perfect_comment + comment + '<br>'
                
            if color == 'red' or color == 'green' or color == 'yellow':
                RGY_perfect += 1
                
        # 個別の色スコアが満点以外の場合
        else:
            try:
                #ランダムに対応する色のコメントを取得
                sql = 'SELECT comment FROM lunch_comment WHERE color = %s AND is_positive = FALSE ORDER BY RAND() LIMIT 1'
                mysql.cur.execute(sql, (color,))
                comment = mysql.cur.fetchone()
            except Exception as e:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
            
            if comment is not None:
                comment = str(comment[0])
                
                # 改善点のコメントは一番低いスコアだった色に対するコメントのみにする
                if bad_score > info['score']:
                    shortage_comment = comment
                    bad_score = info['score']

    if RGY_perfect >= 3:
        comment = '彩が完璧な弁当です。すごい！<br>'
        nakai_perfect_zen = random.choice(nakai_perfect_zen) if nakai_perfect_zen else None
        
        perfect_comment = comment + str(nakai_perfect_zen) + '<br>'
        
    else:
        if len(nakai_perfect_zen) >= 2:
            # ランダムに2つの値を選択
            nakai_perfect_zen = random.sample(nakai_perfect_zen, 2) if nakai_perfect_zen else None
        
        if nakai_perfect_zen is not None:
            for row in nakai_perfect_zen:
                perfect_comment = perfect_comment + str(row) + '<br>'
    
    result_comment = perfect_comment + '<br>' + shortage_comment + '<br>' + sub_comment
    
    # 点数が100点を超えた場合は100点に修正する
    if point_inc >= 100:
        point_inc = 100

    return point_inc,result_comment,color_point,color_point_name_code,color_point_name_jp

# 新しいcsvの作成方法
def write_gen_colors_csv(result):
    csv_path = variable.csv_path  # ここに実際のパスを指定してください
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['gen-colors', '1'])  # ヘッダー行
        color_names = [
            'red', 'orange', 'yellow', 'yellow-green', 'green', 'light-green',
            'green-blue', 'light-blue', 'blue', 'purple', 'pink', 'white',
            'black', 'gray', 'brown'
        ]
        for name in color_names:
            found = False
            for item in result:
                if item[2] == name:
                    writer.writerow([name, item[1]])
                    found = True
                    break
            if not found:
                writer.writerow([name, 0])
