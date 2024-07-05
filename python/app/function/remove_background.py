from flask import Blueprint, render_template, request, redirect
from PIL import Image
import requests, os, io
from function import variable

app = Blueprint('remove_background', __name__)

REMBG_CONTAINER_NAME = os.getenv('REMBG_CONTAINER_NAME')
REMBG_CONTAINER_PORT = os.getenv('REMBG_CONTAINER_PORT')
REMBG_PROCESSING_KEY = os.getenv('REMBG_PROCESSING_KEY')

# タイムアウト時間(秒)
timeout_value = 30

@app.route('/rembg', methods=['POST', 'GET'])
def rembg_route():
    if request.method == 'POST':
        image = request.files['image']
        image.save('./static/images/process_image.jpeg')
        txt = process_image()
        return txt
    else:
        return render_template('image_upload.html')

def process_image(image):
    image = Image.open(image)
    image.save('./static/images/process_image.jpeg')
    send_url = f"http://{REMBG_CONTAINER_NAME}:{REMBG_CONTAINER_PORT}/"
    response = requests.post(send_url, data=REMBG_PROCESSING_KEY, timeout=timeout_value)
    if response.status_code != 200:
        return 'Error: ' + response.text
    else:
        rembg_image = Image.open('./static/images/output.png')
        return rembg_image