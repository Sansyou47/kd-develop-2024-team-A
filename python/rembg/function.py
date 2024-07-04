from PIL import Image, UnidentifiedImageError
from rembg import remove
from http.server import HTTPServer, BaseHTTPRequestHandler
import io, os

port = int(os.getenv('REMBG_CONTAINER_PORT'))

def process_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        image = remove(image)
        return image
    except UnidentifiedImageError:
        print("受け取ったデータは有効な画像ファイルではありません。")
        return None
    except Exception as e:
        print(f"画像処理中に予期せぬエラーが発生しました: {e}")
        return None

class ImageProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        # Content-Lengthヘッダーからデータの長さを取得
        content_length = int(self.headers['Content-Length'])
        image_data = self.rfile.read(content_length)
        processed_image = process_image(image_data)
        
        # 背景処理に失敗した場合、エラーメッセージを返す
        if processed_image is None:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Invalid image data.')
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', len(processed_image))
            self.end_headers()
            self.wfile.write(processed_image)
            
class test(BaseHTTPRequestHandler):
    def do_POSTtest(self):
        # Content-Lengthヘッダーからデータの長さを取得
        content_length = int(self.headers['Content-Length'])
        # データを読み取る
        post_data = self.rfile.read(content_length)
        # バイトデータをデコードしてテキストに変換
        text_data = post_data.decode('utf-8')

        # ここでtext_dataを処理する
        # 例: 受け取ったテキストデータをコンソールに出力
        print(text_data)

        # レスポンスを送信
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'test')

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', port), ImageProcessor)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()