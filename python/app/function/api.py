from flask import Blueprint

app = Blueprint("api", __name__)

app.route('/developers/api', methods=['GET', 'POST'])
def api():
    return "API"