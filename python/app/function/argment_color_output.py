from PIL import Image
from function import variable
import csv

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
    
def write_colors_to_csv(color_codes):
    # CSVファイルを開き、書き込む
    with open(variable.csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # ヘッダーを書き込む
        writer.writerow(['Color Code'])
        # 色コードのリストをループ処理
        for color_code in color_codes:
            # 各色コードをCSVファイルに書き込む
            writer.writerow([color_code])