from PIL import Image
from function import variable
from decimal import Decimal, ROUND_HALF_UP
import csv
import numpy as np
import colorsys
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76

# # 固定された色のRGB値と名前
# fixed_colors_rgb = {
#     'red': (255, 0, 0),
#     'green': (0, 255, 0),
#     'blue': (0, 0, 255),
#     'yellow': (255, 255, 0),
#     'orange': (255, 165, 0),
#     'purple': (128, 0, 128),
#     'white': (255, 255, 255),
#     'black': (0, 0, 0),
#     'gray': (128, 128, 128),
#     'brown': (165, 42, 42)
# }

# 固定された色をCIELAB色空間に変換
fixed_colors_lab = {name: rgb2lab(np.array([[rgb]])) for name, rgb in variable.fixed_colors_rgb.items()}

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
    
# RGB値を16進数形式に変換する関数
def rgb_to_hex(rgb):
    # RGB値を16進数形式に変換
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# 16進数形式の色コードをRGB値に変換する関数
def hex_to_rgb(hex_color):
    # 先頭の'#'を取り除き、RGB値に変換
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
# 色コードと割合のリストをCSVファイルに書き込む関数
def write_colors_to_csv(color_codes_with_ratios, csv_path=variable.csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for color_code, ratio in color_codes_with_ratios:
            # RGB値を16進数形式に変換
            hex_color = rgb_to_hex(color_code)
            
            # 色コードと割合を書き込む
            writer.writerow([hex_color, ratio])
        
# 画像からドミナントカラーを抽出する関数
def extract_dominant_colors(image_path, num_colors=10):
    image = Image.open(image_path)
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

# １６進数の色コードの近似値を求める関数（破棄予定）
def find_nearest_color():
    nearest_colors = []
    with open(variable.csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            hex_value = int(row[0], 16)  # CSVの値を16進数として読み込む
            nearest_color = None
            min_diff = float('inf')  # 最小差分を無限大で初期化
            for color_hex, color_name in variable.color_index.items():
                diff = abs(color_hex - hex_value)  # 差分の絶対値を計算
                if diff < min_diff:
                    min_diff = diff
                    nearest_color = color_name
            nearest_colors.append(nearest_color)
    return nearest_colors

# ２つの色のCIELAB色空間での色差を計算する関数
def classify_color(dominant_color_rgb):
    # ドミナントカラーをCIELAB色空間に変換
    dominant_color_lab = rgb2lab(np.array([[dominant_color_rgb]]))
    
    # 最小の色差とその色を初期化
    min_delta = float('inf')
    closest_color_name = None
    
    # 固定された色との色差を計算
    for name, lab in fixed_colors_lab.items():
        delta = deltaE_cie76(dominant_color_lab, lab)
        if delta < min_delta:
            min_delta = delta
            closest_color_name = name
    
    return closest_color_name

# 12色相環を定義
color_wheel_12 = ['red', 'red-orange', 'yellow-orange',
               'yellow', 'yellow-green', 'green',
               'blue-green', 'blue', 'blue-violet',
               'violet', 'red-violet', 'red']

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
    # 白の閾値（明度がこの値より大きい場合は白と判定）
    white_threshold = 0.85
    # 灰色の閾値（彩度がこの値より小さい場合は灰色と判定）
    gray_saturation_threshold = 0.2
    # 黒の閾値（明度がこの値より小さい場合は黒と判定）
    black_threshold = 0.2
    # 茶色の判定基準
    brown_hue_range = (0, 40)
    brown_saturation_threshold = 0.3
    brown_value_threshold = 0.2

    # 白の判定
    if value > white_threshold and saturation < 0.2:
        return 'white'
    # 黒の判定
    elif value < black_threshold:
        return 'black'
    # 灰色の判定
    elif saturation < gray_saturation_threshold:
        return 'gray'
    # 茶色の判定
    elif brown_hue_range[0] <= hue <= brown_hue_range[1] and saturation > brown_saturation_threshold and value > brown_value_threshold or brown_hue_range[0] <= hue <= brown_hue_range[1]:
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