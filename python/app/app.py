from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from function import pil_demo, variable, blueprint_demo

app = Flask(__name__)

app.register_blueprint(blueprint_demo.app)

# インデックスルート
@app.route('/')
def index():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")