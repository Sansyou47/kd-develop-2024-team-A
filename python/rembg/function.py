from PIL import Image
from rembg import remove
from http.server import HTTPServer, BaseHTTPRequestHandler
import io

def process_image(image_data):
    try:
        # 画像データをPIL.Imageオブジェクトに変換して確認
        image = Image.open(io.BytesIO(image_data))
        image = remove(image_data)
        return image.tobytes()
    except Exception as e:
        print(f"画像処理中にエラーが発生しました: {e}")
        return None

class ImageProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        # Content-Lengthヘッダーからデータの長さを取得
        content_length = int(self.headers['Content-Length'])
        image_data = self.rfile.read(content_length)
        processed_image = process_image(image_data)
        if processed_image:
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', len(processed_image))
            self.end_headers()
            self.wfile.write(processed_image)
        else:
            self.send_error(400, "画像処理に失敗しました。")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 7047), ImageProcessor)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()