import csv

# 画像ファイルのパス(app.pyからの相対パス)
image_path = './static/images/bento_01.jpg'
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
    ['パプリカ（赤）', 'red'],
    ['イチゴ', 'red'],
    ['赤キャベツ', 'red'],
    ['リンゴ', 'red'],
    ['スモモ', 'red'],
    ['赤ピーマン', 'red'],
    ['サーモン', 'red'],
    ['カプレーゼ', 'red'],
    ['チェリートマト', 'red'],
    # ['赤ぶどう', 'red'],
    # ['黒紫蘇', 'red'],
    ['梅干し', 'red'],
    # ['赤リンゴ', 'red'],
    ['ローストビーフ', 'red'],
    ['ハム', 'red'],
    ['ニンジン', 'orange'],
    ['カボチャ', 'orange'],
    ['みかん', 'orange'],
    ['パパイヤ', 'orange'],
    # ['黒ニンジン', 'orange'],
    # ['クルミ', 'orange'],
    # ['白人参', 'orange'],
    # ['白アスパラガス', 'white-orange'],
    ['コーン', 'yellow'],
    ['パプリカ（黄）', 'yellow'],
    ['マンゴー', 'yellow'],
    ['バナナ', 'yellow'],
    ['パイナップル', 'yellow'],
    ['レモン', 'yellow'],
    ['かぼちゃ', 'yellow'],
    ['生姜', 'yellow'],
    ['卵焼き', 'yellow'],
    # ['黒パプリカ（黄）', 'yellow'],
    # ['黒豆もやし', 'yellow'],
    # ['焼きとうもろこし', 'yellow'],
    ['たくあん', 'yellow'],
    # ['白カボチャ', 'yellow'],
    # ['白とうもろこし', 'yellow'],
    ['フライドチキン', 'yellow'],
    # ['ツナサラダ', 'white-yellow'],
    ['チキン南蛮', 'brown'],
    ['ほうれん草', 'green'],
    ['ブロッコリー', 'light-green'],
    ['枝豆', 'yellow-green'],
    ['グリーンピース', 'yellow-green'],
    ['レタス', 'light-green'],
    ['キウイ', 'green'],
    ['ピーマン', 'light-green'],
    ['アボカド', 'green'],
    ['グリーンアップル', 'yellow-green'],
    ['ズッキーニ', 'green-blue'],
    ['ケール', 'light-green'],
    ['スプラウト', 'green'],
    ['小松菜', 'green-blue'],
    ['しそ', 'green'],
    ['エンドウ豆', 'green'],
    ['アスパラガス', 'green'],
    ['パセリ', 'green'],
    # ['青じそ', 'green'],
    # ['ケール（黒）', '黒緑'],
    # ['黒オリーブ', '黒緑'],
    ['ほうれん草のごま和え', 'green'],
    # ['白ほうれん草', '白緑'],
    # ['白セロリ', '白緑'],
    # ['白菜', 'white-green'],
    ['ブルーベリー', 'blue'],
    ['ぶどう','blue'],
    # ['黒アサイー', '黒青'],
    # ['白紫蘇', 'white-blue'],
    # ['白アサイー', 'white-blue'],
    ['なす', 'purple'],
    ['紫キャベツ', 'purple'],
    ['さつまいもの煮物', 'purple'],
    ['紫芋', 'purple'],
    # ['黒ナス', '黒紫'],
    # ['黒イチジク', '黒紫'],
    ['ひじき', 'black'],
    ['黒豆', 'black'],
    ['黒ごま', 'black'],
    ['黒米', 'black'],
    ['海苔', 'black'],
    ['ごはん', 'white'],
    ['大根', 'white'],
    ['豆腐', 'white'],
    ['カリフラワー', 'white'],
    ['豆乳', 'white'],
    ['ヨーグルト', 'white'],
    ['チーズ', 'white'],
    ['マッシュルーム', 'white'],
    ['タケノコ', 'white'],
    ['カニカマサラダ', 'white'],
    ['ポテトサラダ', 'white'],
    ['白ナス', 'white'],
    # ['黒ごま（灰）', 'gray'],
    ['灰もち米', 'gray'],
    ['レンコンきんぴら', 'gray'],
    ['煮しめ', 'gray'],
    ['こんにゃく', 'brown'],
    ['さつまいも', 'brown'],
    ['玄米', 'brown'],
    ['紅茶', 'brown'],
    ['ナッツ', 'brown'],
    ['チョコレート', 'brown'],
    ['コーヒー', 'brown'],
    ['しいたけ', 'brown'],
    ['クルミ', 'brown'],
    ['オートミール', 'brown'],
    ['アーモンド', 'brown'],
    ['ハンバーグ', 'brown'],
    ['筑前煮', 'brown'],
    ['照り焼きチキン', 'brown'],
    ['春巻き', 'brown'],
    ['エビフライ', 'brown'],
    ['鶏の唐揚げ', 'brown'],
    ['もも','pink'],
    ['桜でんぶ','pink'],
    ['マカロン','pink'],
    ['ゼリー(ピンク)','pink'],
    ['コ〇ラのマ〇チ＜ソ〇ダフロ〇ト＞','green-blue'],
    ['ララクラ〇シ〇 ソーダ','green-blue'],
]