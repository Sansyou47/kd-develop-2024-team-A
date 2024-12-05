import requests, json

# API Gatewayのエンドポイント(本番環境では環境変数に保存して使用すること。直打ち禁止)
API_GATEWAY_ENDPOINT = 'https://9z2hi8ksd3.execute-api.ap-northeast-1.amazonaws.com/default/ColorLabeling'

def send_text_to_lambda(text):
    # テキストデータをJSON形式に変換
    text = json.dumps(text)
    # ヘッダーの設定 (必要に応じて変更)
    headers = {
        'Content-Type': 'application/json'
    }

    # POSTリクエストを送信
    response = requests.post(API_GATEWAY_ENDPOINT, data=text, headers=headers)

    # レスポンスのステータスコードをチェック
    if response.status_code == 200:
        print("テキストを送信しました")
        # レスポンスの処理 (必要に応じて)
        result = response.json()
        print(result)
    else:
        print("エラーが発生しました:", response.status_code)

# 送信するテキスト
text_data = [
    '#ffffff',
    '#000000',
    '#ff0000',
    '#00ff00',
    '#0000ff',
    '#ffff00',
    '#ff00ff',
    '#00ffff',
    '#808080',
    '#800000',
    '#008000',
    '#000080',
    '#808000',
    '#800080',
    '#008080',
    '#c0c0c0',
    '#808040',
    '#804000',
    '#408000',
    '#400080',
    '#804080',
    '#408080',
    '#004040',
    '#004080',
    '#400040',
    '#ff8080',
    '#80ff80',
    '#8080ff',
    '#ffff80',
    '#ff80ff',
    '#80ffff',
    '#404040',
    '#ff0000',
    '#00ff00',
    '#0000ff'
]
# 関数を呼び出す
send_text_to_lambda(text_data)