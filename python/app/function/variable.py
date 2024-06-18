# オリジナル画像の保存先
imgLocation_origin = 'images/origin/'
# リサイズ画像の保存先
imgLocation_resized = 'images/downsize/'
# アプリでサポートされている拡張子リスト
supportedExtentionList = ['jpg', 'jpeg', 'png']
# 暗号化された画像の保存先
imgLocation_encrypted = 'images/encrypted/'
# 復号化された画像の保存先
imgLocation_decrypted = 'images/decrypted/'


def xor_enc_dec(input, output, length, secret_key):
    count = 0
    for i in range(length):
        output[i] = input[i] ^ ord(secret_key[count])
        count += 1
        if count == len(secret_key):
            count = 0


def enc_file(inputfile, outputfile, secretKey):
    with open(inputfile, 'rb') as f:
        data = f.read()
    length = len(data)
    data = bytearray(data)
    xor_enc_dec(data, data, length, secretKey)
    with open(outputfile, 'wb') as f:
        f.write(data)


prompt = "お弁当の料理名を羅列し、料理に含まれている具材の一番多い五大栄養素を要素ごとに羅列してください。例:**料理名**鶏の唐揚げ 卵焼き 野菜炒め ブロッコリー プチトマト ご飯**五大栄養素**鶏の唐揚げ炭水化物: 小麦粉タンパク質: 鶏肉脂質: サラダ油ビタミン: レモンミネラル: 塩卵焼き炭水化物: 砂糖タンパク質: 卵脂質: サラダ油ビタミン: 青ネギミネラル: 塩野菜炒め炭水化物: ニンジンタンパク質: 豚肉脂質: サラダ油ビタミン: キャベツミネラル: 塩ブロッコリー炭水化物: ブロッコリータンパク質: ブロッコリー脂質: -ビタミン: ブロッコリーミネラル: ブロッコリープチトマト炭水化物: プチトマトタンパク質: プチトマト脂質: -ビタミン: プチトマトミネラル: プチトマトご飯炭水化物: 米タンパク質: -脂質: -ビタミン: -ミネラル: 塩"
# お弁当の料理名を羅列し、料理に含まれている具材の一番多い五大栄養素を要素ごとに羅列してください。例:料理名：具材1,具材2,具材3,具材4,具材5<br>栄養素：栄養素1,栄養素2,栄養素3,栄養素4,栄養素5,次の料理名を記述する<br>を2回
