from decimal import Decimal, ROUND_HALF_UP
import colorsys
import json

# 12色相環を定義
color_wheel_12 = ['red', 'orange', 'yellow',
               'yellow-green', 'green', 'lime-green',
               'light-blue', 'light-blue', 'blue',
               'purple', 'pink', 'red']

new_color_wheel_12 = ['red', 'orange', 'yellow',
               'yellow-green', 'green', 'lime-green',
               'aqua', 'sky-blue', 'blue',
               'purple', 'pink', 'deep-pink']

# RGBをHSL色空間へ変換する関数
def rgb_to_hsl(rgb_color):
    """
    Args:
        rgb_color (tuple): RGB値のタプル (R, G, B) 各値は0から255の範囲
    Returns:
        tuple: HSL値のタプル (H, S, L)
            H: 色相 (0.0から1.0の範囲)
            S: 彩度 (0.0から1.0の範囲)
            L: 明度 (0.0から1.0の範囲)
    """
    # RGB値を0から1の範囲に正規化
    r, g, b = [x / 255.0 for x in rgb_color]
    
    # 最大値と最小値を取得
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    
    # 明度を計算
    l = (max_c + min_c) / 2

    if max_c == min_c:
        # RGB値が全て同じ場合、色相と彩度は0
        h = s = 0.0
    else:
        # 差分を計算
        d = max_c - min_c
        
        # 彩度を計算
        s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        
        # 色相を計算
        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        elif max_c == b:
            h = (r - g) / d + 4
        h /= 6

    return h, s, l
    
def find_closest_color_hsl(hsl_color):  
    # HSV：Hue（色相）、Saturation（彩度）、Value（明度）
    hue, saturation, luminance = hsl_color
    hue *= 360  # 色相を度に変換
    saturation *= 100
    luminance *= 100
    
    gray_saturation_threshold = 20          # 灰色とする彩度の下限閾値
    white_luminance = 90                    # 白とする明度の上限閾値
    black_luminance = 18                    # 黒とする明度の下限閾値
    
    brown_hue_range = (0, 40, 330, 360)     # 茶色とする色相の幅の閾値
    chromatic_saturation_range = (30, 100)  # 有彩色とする彩度の幅の閾値
    chromatic_luminance_range = (20, 80)    # 有彩色とする明度の幅の閾値
    
    # この範囲内なら有彩色として処理する
    if chromatic_luminance_range[0] <= luminance <= chromatic_luminance_range[1] and chromatic_saturation_range[0] <= saturation <= chromatic_saturation_range[1]:
        # 12色相環の判定（30=360/12）
        index = int(Decimal(hue/30).to_integral_value(rounding=ROUND_HALF_UP)) % 12
        # 閾値内のラベルそれぞれに'dark', 'light'を付与する
        if black_luminance <= luminance <= 35:
            color_label = f'dark-{new_color_wheel_12[index]}'
        elif 35 < luminance <= 65:
            color_label = new_color_wheel_12[index]
        elif 56 < luminance <= white_luminance:
            color_label = f'light-{new_color_wheel_12[index]}'
        else:
            color_label = 'not chromatic'
        
        return color_label
    # 深緑が不明にラベリングされるのを防ぐ
    elif black_luminance <= luminance and luminance <= chromatic_luminance_range[0] and 70 <= hue <= 130:
        return 'green'
    else:
        # 白の判定
        if luminance >= white_luminance:
            return 'white'
        # 黒の判定
        elif luminance <= black_luminance:
            return 'black'
        elif luminance >= chromatic_luminance_range[1]:
            return 'gray'
        elif saturation <= 30 and luminance >= 80:
            return 'gray'
        elif saturation <= gray_saturation_threshold:
            return 'gray'
        elif brown_hue_range[0] <= hue <= brown_hue_range[1] and luminance <= 45:
            return 'brown'
        elif brown_hue_range[2] <= hue <= brown_hue_range[3] and luminance <= 45:
            return 'brown'
        else:
            return 'not chromatic'
        
def lambda_handler(event, context):
    data = event['body']
    hex_colors_list = json.loads(data)
    
    if not hex_colors_list:
        return {
            'statusCode': 400,
            'body': json.dumps('hex_color is required')
        }
        
    colors_label_list = []
    
    for hex_color in hex_colors_list:
        if isinstance(hex_color, str):
            hex_color = hex_color.lstrip('#')
            print(f'hex_color:{hex_color}')
            rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
            print(f'rgb_color:{rgb_color}')

            hsl_color = rgb_to_hsl(rgb_color)
            color_label = find_closest_color_hsl(hsl_color)
            colors_label_list.append(color_label)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid hex color format')
            }
    
    # 結果を返す
    return {
        'statusCode': 200,
        'body': json.dumps({'color_label': colors_label_list})
    }