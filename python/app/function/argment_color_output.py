from PIL import Image
from function import variable
import csv
import numpy as np
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

# # 画像ファイルのパスを指定
# image_path = 'path/to/your/image.jpg'
# dominant_colors = extract_dominant_colors(image_path)

# # 結果を出力
# print("Dominant colors (RGB):")
# for color in dominant_colors:
#     print(color)