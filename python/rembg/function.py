from PIL import Image, UnidentifiedImageError
from rembg import remove
from http.server import HTTPServer, BaseHTTPRequestHandler
import io, os, json

PORT = int(os.getenv('REMBG_CONTAINER_PORT'))
PROCESSING_KEY = os.getenv('REMBG_PROCESSING_KEY')

def remove_background(filename):
    try:
        image_path = f'./images/original/{filename}.jpeg'
        image = Image.open(image_path)
        image = remove(image)
        output_image_path = f'./images/processed/{filename}.png'
        image.save(output_image_path)
    except Exception as e:
        print(f"画像処理中に予期せぬエラーが発生しました: {e}")
        return 'procces error.'
    else:
        return 'process success.'

class ImageProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        # Content-Lengthヘッダーからデータの長さを取得
        content_length = int(self.headers['Content-Length'])
        # データを読み取る
        post_data = self.rfile.read(content_length)
        # バイトデータをデコードしてテキストに変換
        data = json.loads(post_data.decode('utf-8'))
        
        received_key = data.get('processing_key')
        filename = data.get('filename')
        
        if received_key == PROCESSING_KEY:
            message = remove_background(filename)
            if message == 'process success.':
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                return
            else:
                print('画像処理中にエラーが発生しました。')
                self.send_response(500)
                self.end_headers()
                return
        else:
            print('認証キーが一致しません。')
            self.send_response(401)
            self.end_headers()
            return

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), ImageProcessor)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()