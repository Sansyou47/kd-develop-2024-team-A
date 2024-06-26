from flask import Blueprint, render_template, request
from PIL import Image
from function import variable
from decimal import Decimal, ROUND_HALF_UP
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
def extract_dominant_colors(image, num_colors=30):
    image = Image.open(image)
    #画像がRGBでない場合、RGBに変換
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = np.array(image).reshape(-1, 3)
    
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
    return [(tuple(color), ratio) for color, ratio in zip(dominant_colors, color_ratios)]

# 12色相環を定義
color_wheel_12 = ['red', 'orange', 'yellow',
               'yellow-green', 'green', 'light-green',
               'green-blue', 'light-blue', 'blue',
               'purple', 'pink', 'red']

# 24色相環を定義
color_wheel_24 = ['red', 'vermilion', 'orange', 'amber', 'yellow', 'yellow-green',
               'green', 'spring-green', 'cyan', 'sky-blue', 'blue', 'ultramarine',
               'violet', 'purple', 'magenta', 'rose', 'crimson', 'raspberry',
               'burgundy', 'rust', 'tangerine', 'apricot', 'beige', 'peach']

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

    # 結果を返す
    return str(missing) + 'が不足しています。'

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
    

@app.route('/colors', methods=['GET', 'POST'])
def pil():
    if request.method == 'POST':
        image = request.files['image']
        colors = extract_dominant_colors(image)
        write_colors_to_csv(colors)

        colors_list = []
        for color_code, ratio in colors:
            # RGB値を16進数形式に変換
            hex_color = '#{:02x}{:02x}{:02x}'.format(color_code[0], color_code[1], color_code[2])
            colors_list.append([hex_color, ratio])

        judged_colors_list = judge_color(colors_list)
        
        # return 'judged_colors_list=' + str(judged_colors_list) + '<br>' + 'colors_list=' + str(colors_list)
        colors_code = [item[0] for item in colors_list]
        colors_per = [float(item[1]) for item in colors_list]
        colors_name = [item[1] for item in judged_colors_list]
        result = []
        for i in range(len(judged_colors_list)):
            result.append([colors_code[i], colors_per[i], colors_name[i]])
        Shortage_result = Shortage(missing_color(colors_name))

        #resultをソートして別々のリストに取り出す
        result.sort(key=lambda x: x[1], reverse=True)
        colors_code = [item[0] for item in result]
        colors_per = [item[1] for item in result]
        colors_name = [item[2] for item in result]

        return render_template('output_colors.html', result = result, Shortage_result = Shortage_result, colors_code = colors_code, colors_per = colors_per, colors_name = colors_name ) 
    else:
        return render_template('judge_color.html')