from flask import Blueprint, render_template
import os, subprocess, re, random
from function import variable

app = Blueprint('easter_egg', __name__)

@app.route('/contact')
def contact():
    # ランダムにキャラクターを選択
    charactor = variable.cowsayCharacters[random.randint(0, len(variable.cowsayCharacters) - 1)]
    # cowsayコマンドを実行
    result = subprocess.run(['/usr/games/cowsay', '-f', charactor, 'コンタクトは取れないヨ！'], encoding='utf-8', stdout=subprocess.PIPE)
    # 連続する空白を&nbsp;に置換
    formatted_text = re.sub(r' {2,}', lambda match: '&nbsp;' * len(match.group()), result.stdout)
    # 改行を<br>タグに置換
    formatted_text = formatted_text.replace('\n', '<br>')
    # 置換したテキストをHTMLに渡す
    return render_template('out.html', text=formatted_text)