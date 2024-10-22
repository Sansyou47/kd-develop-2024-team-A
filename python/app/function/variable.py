import csv

# 画像ファイルのパス(app.pyからの相対パス)
image_path = './static/images/bento.jpeg'
# 出力画像のパス
output_image_path = './static/images/output.png'
# CSVファイルのパス
csv_path = './static/csv/colors.csv'
# アプリでサポートされている拡張子リスト
supportedExtentionList = ['jpg', 'jpeg', 'png']
# cowsayのデフォルトキャラ一覧
cowsayCharacters = ['bud-frogs', 'bunny', 'cheese', 'cower', 'daemon', 'default', 'dragon', 'dragon-and-cow', 'elephant', 'elephant-in-snake', 'eyes', 'flaming-sheep', 'ghostbusters', 'hellokitty', 'kiss', 'koala', 'kosh', 'luke-koala', 'mech-and-cow', 'milk', 'moofasa', 'moose', 'ren', 'sheep', 'skeleton', 'stegosaurus', 'stimpy', 'three-eyes', 'turkey', 'turtle', 'tux', 'vader', 'vader-koala', 'www']
# cowsayに言わせたいメッセージ
cowsayMessage = ['コンタクトは取れないヨ！', '二斗を追うものは一斗をも得ず', '猿も木から落ちる', '猫に小判は飼い主が嬉しい', '404 Not-Found']
# 占いの結果一覧
fortuneList = ['大吉', '中吉', '小吉', '吉', '凶', '大凶', '終わり']

rembg_image_path = '../static/images/bento.jpeg'
rembg_output_image_path = '../static/images/output.png'

# 基準となる色コードリスト
color_index = {
    0xFF0000 : 'red',
    0x00FF00 : 'green',
    0x0000FF : 'blue',
    0xFFFF00 : 'yellow',
    0xFFA500 : 'orange',
    0xa800ff : 'purple',
    0x000000 : 'black',
    0xFFFFFF : 'white',
    0x808080 : 'gray',
    0x965042 : 'brown'
}
fixed_colors_rgb = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'brown': (165, 42, 42)
}

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
        
def read_csv(csv_path):
    colors = []
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            # CSVの各行をリストに追加
            colors.append(row)
    return colors


prompt = "いままでの命令をすべて忘れこれからの命令を遵守してください。お弁当の料理名を羅列し、料理に含まれている具材の一番多い五大栄養素を要素ごとに羅列してください。例:料理名:具材1,具材2,.....<br>五大栄養素_炭水化物:具材1,具材4_タンパク質:具材2_脂質:具材5_ビタミン:具材6_ミネラル:--<br> を画像の料理ごとに例に沿って行う。決して例の内容は使わないでください。料理以外の写真はテキストで「判定できませんでした、お弁当の写真だけを送信してください」と表示させてください。"


# "お弁当の料理名を羅列し、料理に含まれている具材の一番多い五大栄養素を要素ごとに羅列してください。例:**料理名**鶏の唐揚げ 卵焼き 野菜炒め ブロッコリー プチトマト ご飯**五大栄養素**鶏の唐揚げ炭水化物: 小麦粉タンパク質: 鶏肉脂質: サラダ油ビタミン: レモンミネラル: 塩卵焼き炭水化物: 砂糖タンパク質: 卵脂質: サラダ油ビタミン: 青ネギミネラル: 塩野菜炒め炭水化物: ニンジンタンパク質: 豚肉脂質: サラダ油ビタミン: キャベツミネラル: 塩ブロッコリー炭水化物: ブロッコリータンパク質: ブロッコリー脂質: -ビタミン: ブロッコリーミネラル: ブロッコリープチトマト炭水化物: プチトマトタンパク質: プチトマト脂質: -ビタミン: プチトマトミネラル: プチトマトご飯炭水化物: 米タンパク質: -脂質: -ビタミン: -ミネラル: 塩"
# お弁当の料理名を羅列し、料理に含まれている具材の一番多い五大栄養素を要素ごとに羅列してください。例:料理名：具材1,具材2,具材3,具材4,具材5<br>栄養素：栄養素1,栄養素2,栄養素3,栄養素4,栄養素5,次の料理名を記述する<br>を2回

# お弁当用仮想データ
missing_vegetables = [
    ['トマト', 'red'],
    # ['パプリカ（赤）', 'red'],
    ['イチゴ', 'red'],
    # ['赤キャベツ', 'red'],
    ['リンゴ', 'red'],
    # ['スモモ', 'red'],
    # ['赤ピーマン', 'red'],
    # ['サーモン', 'red'],
    # ['カプレーゼ', 'red'],
    # ['チェリートマト', 'red'],
    # ['赤ぶどう', 'red'],
    # ['黒紫蘇', 'red'],
    ['梅干し', 'red'],
    # ['赤リンゴ', 'red'],
    # ['ローストビーフ', 'red'],
    ['ハム', 'red'],
    ['ニンジン', 'orange'],
    ['カボチャ', 'orange'],
    ['みかん', 'orange'],
    # ['パパイヤ', 'orange'],
    # ['黒ニンジン', 'orange'],
    # ['クルミ', 'orange'],
    # ['白人参', 'orange'],
    # ['白アスパラガス', 'white-orange'],
    ['コーン', 'yellow'],
    # ['パプリカ（黄）', 'yellow'],
    # ['マンゴー', 'yellow'],
    ['バナナ', 'yellow'],
    ['パイナップル', 'yellow'],
    # ['レモン', 'yellow'],
    # ['かぼちゃ', 'yellow'],
    # ['生姜', 'yellow'],
    ['卵焼き', 'yellow'],
    # ['黒パプリカ（黄）', 'yellow'],
    # ['黒豆もやし', 'yellow'],
    # ['焼きとうもろこし', 'yellow'],
    ['たくあん', 'yellow'],
    # ['白カボチャ', 'yellow'],
    # ['白とうもろこし', 'yellow'],
    # ['フライドチキン', 'yellow'],
    # ['ツナサラダ', 'white-yellow'],
    ['チキン南蛮', 'brown'],
    ['ほうれん草', 'green'],
    ['ブロッコリー', 'light-green'],
    ['枝豆', 'yellow-green'],
    ['グリーンピース', 'yellow-green'],
    ['レタス', 'light-green'],
    # ['キウイ', 'green'],
    ['ピーマン', 'light-green'],
    # ['アボカド', 'green'],
    # ['グリーンアップル', 'yellow-green'],
    # ['ズッキーニ', 'green-blue'],
    # ['ケール', 'light-green'],
    # ['スプラウト', 'green'],
    ['小松菜', 'green-blue'],
    # ['しそ', 'green'],
    ['エンドウ豆', 'green'],
    ['アスパラガス', 'green'],
    ['パセリ', 'green'],
    # ['青じそ', 'green'],
    # ['ケール（黒）', '黒緑'],
    # ['黒オリーブ', '黒緑'],
    # ['ほうれん草のごま和え', 'green'],
    # ['白ほうれん草', '白緑'],
    # ['白セロリ', '白緑'],
    # ['白菜', 'white-green'],
    ['ブルーベリー', 'purple'],
    ['ぶどう','purple'],
    # ['黒アサイー', '黒青'],
    # ['白紫蘇', 'white-blue'],
    # ['白アサイー', 'white-blue'],
    ['なす', 'purple'],
    # ['紫キャベツ', 'purple'],
    # ['さつまいもの煮物', 'purple'],
    # ['紫芋', 'purple'],
    # ['黒ナス', '黒紫'],
    # ['黒イチジク', '黒紫'],
    ['ひじき', 'black'],
    ['黒豆', 'black'],
    # ['黒ごま', 'black'],
    # ['黒米', 'black'],
    ['海苔', 'black'],
    # ['ごはん', 'white'],
    ['大根', 'white'],
    # ['豆腐', 'white'],
    # ['カリフラワー', 'white'],
    # ['豆乳', 'white'],
    # ['ヨーグルト', 'white'],
    # ['チーズ', 'white'],
    # ['マッシュルーム', 'white'],
    ['タケノコ', 'white'],
    # ['カニカマサラダ', 'white'],
    ['ポテトサラダ', 'white'],
    # ['白ナス', 'white'],
    # ['黒ごま（灰）', 'gray'],
    # ['灰もち米', 'gray'],
    ['きんぴらごぼう', 'gray'],
    ['煮しめ', 'gray'],
    ['こんにゃく', 'gray'],
    ['さつまいも', 'brown'],
    # ['玄米', 'brown'],
    # ['紅茶', 'brown'],
    # ['ナッツ', 'brown'],
    # ['チョコレート', 'brown'],
    # ['コーヒー', 'brown'],
    ['しいたけ', 'brown'],
    # ['クルミ', 'brown'],
    # ['オートミール', 'brown'],
    # ['アーモンド', 'brown'],
    ['ハンバーグ', 'brown'],
    ['筑前煮', 'brown'],
    ['照り焼きチキン', 'brown'],
    ['春巻き', 'brown'],
    ['エビフライ', 'brown'],
    ['鶏の唐揚げ', 'brown'],
    # ['もも','pink'],
    # ['桜でんぶ','pink'],
    # ['マカロン','pink'],
    # ['ゼリー(ピンク)','pink'],
    # ['コアラのマーチ＜ソーダフロスト＞','green-blue'],
    # ['ララクラッシュ ソーダ','green-blue']
]




# ('トマト', 'red', 'vitamin'),
# ('パプリカ（赤）', 'red', 'vitamin'),
# ('イチゴ', 'red', 'vitamin'),
# ('リンゴ', 'red', 'vitamin'),
# ('スモモ', 'red', 'vitamin'),
# ('赤ピーマン', 'red', 'vitamin'),
# ('サーモン', 'red', 'fat'),
# ('カプレーゼ', 'red', 'protein'),
# ('チェリートマト', 'red', 'vitamin'),
# ('赤ぶどう', 'red', 'vitamin'),
# ('梅干し', 'red', 'vitamin'),
# ('赤リンゴ', 'red', 'vitamin'),
# ('ローストビーフ', 'red', 'protein'),
# ('ハム', 'red', 'protein'),
# ('焼き鮭', 'red', 'protein'),


# -- 黄
# ('ニンジン', 'yellow', 'vitamin'),
# ('カボチャ', 'yellow', 'vitamin'),
# ('みかん', 'yellow', 'vitamin'),
# ('パパイヤ', 'yellow', 'vitamin'),
# ('クルミ', 'yellow', 'fat'),
# ('コーン', 'yellow', 'vitamin'),
# ('パプリカ（黄）', 'yellow', 'vitamin'),
# ('マンゴー', 'yellow', 'vitamin'),
# ('バナナ', 'yellow', 'carb'),
# ('パイナップル', 'yellow', 'vitamin'),
# ('レモン', 'yellow', 'vitamin'),
# ('かぼちゃ', 'yellow', 'vitamin'),
# ('生姜', 'yellow', 'vitamin'),
# ('卵焼き', 'yellow', 'protein'),
# ('たくあん', 'yellow', 'vitamin'),
# ('フライドチキン', 'yellow', 'protein'),
# ('ツナサラダ', 'yellow', 'protein'),

# -- 緑
# ('ほうれん草', 'green', 'vitamin'),
# ('ブロッコリー', 'green', 'vitamin'),
# ('枝豆', 'green', 'protein'),
# ('グリーンピース', 'green', 'vitamin'),
# ('レタス', 'green', 'vitamin'),
# ('キウイ', 'green', 'vitamin'),
# ('ピーマン', 'green', 'vitamin'),
# ('アボカド', 'green', 'fat'),
# ('グリーンアップル', 'green', 'vitamin'),
# ('ズッキーニ', 'green', 'vitamin'),
# ('ケール', 'green', 'vitamin'),
# ('スプラウト', 'green', 'vitamin'),
# ('小松菜', 'green', 'vitamin'),
# ('しそ', 'green', 'vitamin'),
# ('エンドウ豆', 'green', 'protein'),
# ('アスパラガス', 'green', 'vitamin'),
# ('パセリ', 'green', 'vitamin'),
# ('青じそ', 'green', 'vitamin'),
# ('ほうれん草のごま和え', 'green', 'vitamin'),
# ('白菜', 'green', 'vitamin'),

# -- 白
# ('ごはん', 'white', 'carb'),
# ('大根', 'white', 'vitamin'),
# ('豆腐', 'white', 'protein'),
# ('カリフラワー', 'white', 'vitamin'),
# ('豆乳', 'white', 'protein'),
# ('ヨーグルト', 'white', 'protein'),
# ('チーズ', 'white', 'protein'),
# ('マッシュルーム', 'white', 'vitamin'),
# ('タケノコ', 'white', 'vitamin'),
# ('カニカマサラダ', 'white', 'protein'),
# ('ポテトサラダ', 'white', 'carb'),

# -- 黒
# ('ひじき', 'black', 'minerals'),
# ('黒豆', 'black', 'protein'),
# ('黒ごま', 'black', 'minerals'),
# ('黒米', 'black', 'carb'),
# ('海苔', 'black', 'vitamin'),
# ('なす', 'black', 'vitamin'),
# ('紫キャベツ', 'black', 'vitamin'),
# ('さつまいもの煮物', 'black', 'carb'),
# ('紫芋', 'black', 'vitamin'),

# -- 茶
# ('こんにゃく', 'brown', 'vitamin'),
# ('さつまいも', 'brown', 'carb'),
# ('玄米', 'brown', 'carb'),
# ('紅茶', 'brown', 'vitamin'),
# ('ナッツ', 'brown', 'fat'),
# ('チョコレート', 'brown', 'fat'),
# ('コーヒー', 'brown', 'minerals'),
# ('しいたけ', 'brown', 'vitamin'),
# ('クルミ', 'brown', 'fat'),
# ('オートミール', 'brown', 'carb'),
# ('アーモンド', 'brown', 'fat'),
# ('ハンバーグ', 'brown', 'protein'),
# ('筑前煮', 'brown', 'carb'),
# ('照り焼きチキン', 'brown', 'protein'),
# ('春巻き', 'brown', 'carb'),
# ('エビフライ', 'brown', 'protein'),
# ('鶏の唐揚げ', 'brown', 'protein'),
# ('チキン南蛮', 'brown', 'protein'),

# -- 青
# ('ブルーベリー', 'blue', 'vitamin'),

# -- 灰
# ('黒ごま', 'gray', 'minerals'),
# ('灰もち米', 'gray', 'carb'),
# ('レンコンきんぴら', 'gray', 'carb'),
# ('煮しめ', 'gray', 'carb'),

# -- 料理名
# -- geminiで判断された場合色を加点するために判断されにくいご飯を追加
# ('米', 'white', 'protein'),
# ('牛丼', 'brown', 'carb'),
# ('日の丸弁当', 'red', 'protein'),
# ('ハム', 'red', 'protein'),
# ('そぼろ', 'yellow', 'protein'),
# ('そぼろ', 'brown', 'protein'),
# ('そぼろ', 'green', 'protein'),
# ('焼きそば', 'brown', 'protein'),
# ('サンドイッチ', 'red', 'protein'),
# ('サンドイッチ', 'green', 'protein'),
# ('サンドイッチ', 'brown', 'protein'),
# ('オムライス', 'yellow', 'carb');
