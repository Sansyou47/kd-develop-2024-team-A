import os
import requests
from flask import Blueprint
# Import the Python SDK
import google.generativeai as genai

API_KEY = os.getenv("gemini_api_key")
genai.configure(api_key=API_KEY)

app = Blueprint("gemini_demo", __name__)

@app.route('/gemini')
def gemini():
    # model = genai.GenerativeModel('gemini-pro')
    
    # response = model.generate_content("3+3の答えを10文字以内で答えてください。")
    # return response.text
    return "hoge"