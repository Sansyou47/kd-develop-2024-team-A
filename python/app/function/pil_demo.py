# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np

def reduce_color_depth(image, nbits):
    """入力された画像の色を指定されたビット数まで下げる

    Args:
        image (PIL.Image.Image): 処理対象の画像
        nbits (int): 色のビット数

    Returns:
        PIL.Image.Image: 色を下げた画像
    """

    # 画像をRGBモードに変換
    image = image.convert('RGB')

    # 画像データをNumPy配列に変換
    image_data = np.array(image)

    # 各ピクセルのRGB値をビット数まで下げる
    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            for k in range(3):
                image_data[i, j, k] = (image_data[i, j, k] >> (8 - nbits)) << (8 - nbits)

    # NumPy配列を画像データに戻す
    image_data = Image.fromarray(image_data.astype('uint8'))

    return image_data

def rrr():
    # 入力画像を読み込む
    input_image = Image.open('function/images/input.jpg')

    # 色を5bitまで下げる
    output_image = reduce_color_depth(input_image, 4)

    # 出力画像を保存する
    output_image.save('function/images/output.jpg')

# from PIL import Image
# from function import variable

# def imgResize(imgName, weight, qlv):
#     img = Image.open(variable.imgLocation_origin + imgName)
#     # 画像の解像度を取得
#     before = img.size
    
#     ext = imgName.split('.')[-1]

#     # 拡大・縮小の倍率を計算
#     multiple = before[0] / weight

#     # 元のアス比でリサイズ解像度を計算
#     after = (weight, int(before[1] / multiple))
    
#     # リサイズ処理
#     img_resized = img.resize(after)
    
#     # メタデータの生成
#     meta = meta_generate(before, after, qlv)
    
#     imgName = imgName.split('.')[0]

#     if ext == 'jpeg' or ext == 'jpg':
#         ext = '.jpg'
#         # リサイズ画像を保存（ファイル名にメタデータを付与）
#         img_resized.save(variable.imgLocation_resized + imgName + str(meta) + ext, quality=qlv)
#     elif ext == 'png':
#         ext = '.png'
#         # リサイズ画像を保存（ファイル名にメタデータを付与）
#         img_resized.save(variable.imgLocation_resized + imgName + str(meta) + ext)
    

# # メタデータ生成関数
# def meta_generate(src_before, src_after, qlv):
#     if src_before[0] > src_after[0]:
#         dmeta = '_(downsizing_'
#     else:
#         dmeta = '_(enlargement_'
#     dmeta += 'resolution=' + str(src_after[0]) + 'x' + str(src_after[1]) + '_'
#     dmeta += 'quality=' + str(qlv) + ')'
    
#     return dmeta

