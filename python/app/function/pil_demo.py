from PIL import Image
from function import variable

def imgResize(imgName, weight, qlv):
    img = Image.open(variable.imgLocation_origin + imgName)
    # 画像の解像度を取得
    before = img.size
    
    ext = imgName.split('.')[-1]

    # 拡大・縮小の倍率を計算
    multiple = before[0] / weight

    # 元のアス比でリサイズ解像度を計算
    after = (weight, int(before[1] / multiple))
    
    # リサイズ処理
    img_resized = img.resize(after)
    
    # メタデータの生成
    meta = meta_generate(before, after, qlv)
    
    imgName = imgName.split('.')[0]

    if ext == 'jpeg' or ext == 'jpg':
        ext = '.jpg'
        # リサイズ画像を保存（ファイル名にメタデータを付与）
        img_resized.save(variable.imgLocation_resized + imgName + str(meta) + ext, quality=qlv)
    elif ext == 'png':
        ext = '.png'
        # リサイズ画像を保存（ファイル名にメタデータを付与）
        img_resized.save(variable.imgLocation_resized + imgName + str(meta) + ext)
    

# メタデータ生成関数
def meta_generate(src_before, src_after, qlv):
    if src_before[0] > src_after[0]:
        dmeta = '_(downsizing_'
    else:
        dmeta = '_(enlargement_'
    dmeta += 'resolution=' + str(src_after[0]) + 'x' + str(src_after[1]) + '_'
    dmeta += 'quality=' + str(qlv) + ')'
    
    return dmeta