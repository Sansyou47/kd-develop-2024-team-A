from PIL import Image
from function import variable
import csv
import numpy as np
from sklearn.cluster import KMeans

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
    
def rgb_to_hex(rgb):
    # RGB値を16進数形式に変換
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
# 色コードと割合のリストをCSVファイルに書き込む関数
def write_colors_to_csv(color_codes_with_ratios, csv_path=variable.csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Color Code', 'Ratio'])
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

# # 画像ファイルのパスを指定
# image_path = 'path/to/your/image.jpg'
# dominant_colors = extract_dominant_colors(image_path)

# # 結果を出力
# print("Dominant colors (RGB):")
# for color in dominant_colors:
#     print(color)