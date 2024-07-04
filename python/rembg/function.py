from PIL import Image, UnidentifiedImageError
from rembg import remove
from http.server import HTTPServer, BaseHTTPRequestHandler
import io, os

PORT = int(os.getenv('REMBG_CONTAINER_PORT'))
PROCESSING_KEY = os.getenv('REMBG_PROCESSING_KEY')

def remove_background():
    try:
        image = Image.open('./images/process_image.jpeg')
        image = remove(image)
        image.save('./images/output.png')
    except Exception as e:
        print(f"画像処理中に予期せぬエラーが発生しました: {e}")
        return 'procces error.'
    else:
        return '0'

class ImageProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        # Content-Lengthヘッダーからデータの長さを取得
        content_length = int(self.headers['Content-Length'])
        # データを読み取る
        post_data = self.rfile.read(content_length)
        # バイトデータをデコードしてテキストに変換
        received_key = post_data.decode('utf-8')
        
        if received_key == PROCESSING_KEY:
            message = remove_background()
            print(message)
        else:
            message = "認証キーが一致しません。"
            print(message)

        # レスポンスを送信
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), ImageProcessor)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()