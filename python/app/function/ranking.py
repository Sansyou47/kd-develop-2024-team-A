from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from function import mysql
import re

# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("ranking", __name__)