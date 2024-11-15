from flask import Blueprint, render_template, request
from PIL import Image
from function import variable, remove_background
from decimal import Decimal, ROUND_HALF_UP
# from rembg import remove
import csv
import numpy as np
import colorsys
from sklearn.cluster import KMeans
import re, base64
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
def extract_dominant_colors(image, num_colors=30):
    # process_image関数へ画像を渡し、背景除去後の画像を取得
    removebg_image, image_name = remove_background.process_image(image)

    #画像がRGBでない場合、RGBに変換
    if removebg_image.mode != 'RGB':
        removebg_image = removebg_image.convert('RGB')

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
        'red': {'threshold': 6, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'yellow': {'threshold': 28, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'green': {'threshold': 9, 'points': 20, 'score': 0,'per':0,'bar_point':0},
        'white': {'threshold': 10, 'points': 10, 'score': 0,'per':0,'bar_point':0},
        'black': {'threshold': 10, 'points': 10, 'score': 0,'per':0,'bar_point':0},
        'brown': {'threshold': 10, 'points': 20, 'score': 0,'per':0,'bar_point':0},
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
            info['bar_point'] = round(info['points'] * proportion,0)
        #それ以外の色の場合の計算
        else:
            info['score'] = max(info['points'] - int((info['threshold'] - info['per']) / 0.4), 0)
            # 棒グラフ計算
            proportion = info['per'] / info['threshold']
            info['bar_point'] = round(info['points'] * proportion,0)
        #点数を加算
        point_inc += info['score']

    #各色の点数を100点満点に変換
    for color, info in colors_info.items():
        #pointsが20点の場合、multipleは5
        multiple = 100 / info['points']
        #100点満点に変換
        info['points'] = 100
        #scoreをmultiple倍する
        info['bar_point'] *= multiple
        #scoreを整数に変換
        info['bar_point'] = int(info['bar_point'])
    
    #htmlに完璧と足りていないから1つ取って 完璧リスト 足りていないリスト
    nakai_color_zen = []
    nakai_perfect_zen = []
    nakai_shortage_zen = []
    color_point = [] #色の点数
    color_point_name_code = [] #色の点数のカラーコード
    color_point_name_jp = [] #色の点数の日本語名
    red_perfect = False
    green_perfect = False

    for color, info in colors_info.items():
        #色の表示
        #reason.append(f'{color_names_jp[color]}色が{info["score"]}/{info["points"]}です。')
        #reason.append({color:info["score"]})
        color_point.append(info["bar_point"])
        color_point_name_code.append(color_names_code[color])
        color_point_name_jp.append(color_names_jp[color])
        #閾値と%の差を計算
        #Conditions = round(info['threshold'] - info['per'], 2)
        #閾値と%の差が0より大きい場合
        #半分以上場合
        if info['score'] == info['points']:
            if color == 'red':
                red_perfect = True
            elif color == 'yellow':
                nakai_perfect_zen.append('黄色は視覚的に美味しそうであったり食欲をそそるといったイメージを持ちやすいです。<br>また、ポジティブな印象を与えることが多いです。<br>これらは食べたいという感情に繋がるだけでなく、盛り付けた際の印象が良くなり、お弁当がより魅力的になります。')
            elif color == 'green':
                green_perfect = True
            # elif color == 'white':
            #     nakai_color_zen.append('白色が足りていません。')
            # elif color == 'black':
            #     nakai_color_zen.append('黒色が足りていません。')
            elif color == 'brown':
                nakai_perfect_zen.append('茶色は肉、揚げ物等の美味しいと感じる傾向にある物が連想されやすい色です。<br>そのため食欲を増加させるのに効果的な色です。')
            # elif color == 'gray':
            #     nakai_color_zen.append('灰色が足りていません。')
        #半分以下の場合
        else:
            
            if color == 'red':
                nakai_shortage_zen.append('暖色系の色は食べ物のうま味を強調し、料理の見栄えを良くします。<br>また、美味しそうな印象を与える効果があり、より良いお弁当になります。')
            elif color == 'yellow':
                nakai_shortage_zen.append('暖色系の色は食べ物のうま味を強調し、料理の見栄えを良くします。<br>また、美味しそうな印象を与える効果があり、より良いお弁当になります。')
            elif color == 'green':
                nakai_shortage_zen.append('もう少し緑野菜を増やすと良いでしょう。<br>野菜は視覚的にも美しく、栄養価も高いため、バランスの良いお弁当になります。')
        
        # 赤と緑の両方が完璧な場合に特定の文章を追加し、個別の文章を追加しない
    if red_perfect and green_perfect:
        nakai_perfect_zen.append('緑と赤による補色は視覚的に元気や明るさといった前向きなイメージを持ちやすいです。<br>そのためポジティブな印象を与えることが多いです。<br>これらは美味しそうで食べたいといった食欲を増加させる感情に繋がりお弁当を良いものにするために不可欠です。')
        nakai_perfect_zen.append('緑と赤による補色は視覚的に元気や明るさといった前向きなイメージを持ちやすいです。<br>そのためポジティブな印象を与えることが多いです。<br>これらは美味しそうで食べたいといった食欲を増加させる感情に繋がりお弁当を良いものにするために不可欠です。')
    else:
        if red_perfect:
            nakai_perfect_zen.append('赤色はうま味や甘みを強調する食欲増進効果と華やかな印象を与えます。<br>緑と組み合わせると視覚的なバランスが取れ、爽やかさと自然な印象が加わります。<br>これにより、料理全体がより魅力的に見え、食欲をさらに刺激します。')
        if green_perfect:
            nakai_perfect_zen.append('緑色は新鮮で健康的なイメージを与えます。<br>他にも料理の色味を補う役目もあり、食欲をそそる視覚効果を生み出します。')
            # elif color == 'white':
            #     nakai_color_zen.append('白色が足りていません。')
            # elif color == 'black':
            #     nakai_color_zen.append('黒色が足りていません。')
            # elif color == 'brown':
            #     nakai_color_zen.append('茶色が足りていません。')
            # elif color == 'gray':
            #     nakai_color_zen.append('灰色が足りていません。')

    # ランダムに1つの値を選択
    nakai_perfect_zen = random.choice(nakai_perfect_zen) if nakai_perfect_zen else None
    nakai_shortage_zen = random.choice(nakai_shortage_zen) if nakai_shortage_zen else None

    # 2つの値をリストに格納
    nakai_color_zen = [nakai_perfect_zen, nakai_shortage_zen]
    # リストの要素を文字列として連結
    nakai_color_zen = '<br>'.join([zen for zen in nakai_color_zen if zen])
    # リストの各要素を改行文字で連結colorのほう
    #concatenated_reasons = ''.join([reason[i] + ('<br>' if i % 2 == 1 else '') for i in range(len(reason))])
    # 不要な文字を削除
    #reason = concatenated_reasons
    
    # 点数が100点を超えた場合は100点に修正する
    if point_inc >= 100:
        point_inc = 100

    return point_inc,nakai_color_zen,color_point,color_point_name_code,color_point_name_jp

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
