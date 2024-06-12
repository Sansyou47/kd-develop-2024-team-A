import os
import requests
from pathlib import Path
from flask import Blueprint
# Import the Python SDK with an alias
import google.generativeai as genai

app = Blueprint("gemini_demo", __name__)

API_KEY = os.getenv('gemini_api_key')

@app.route('/gemini')
def gemini():
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content("3+3の答えを10文字以内で答えてください。")
    return response.text

@app.route('/gemini/image')
def gemini_image():
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel('gemini-pro-vision')

    picture = [{
        'mime_type': 'image/jpeg',
        'data': Path('function/images/image.jpg').read_bytes()
    }]
    prompt = "この画像には何が写っていますか？:"

    response = model.generate_content(
        contents=[prompt, picture[0]]
    )
    return response.text