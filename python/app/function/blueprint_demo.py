from flask import Blueprint

app = Blueprint("blueprint_demo", __name__)

@app.route('/blueprint')
def blueprint():
    return "Hello, Blueprint!"