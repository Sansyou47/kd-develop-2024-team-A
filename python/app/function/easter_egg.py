from flask import Blueprint, render_template, request, redirect
import os, subprocess, re, random
from function import variable

app = Blueprint('easter_egg', __name__)

# @app.route('/variable/test/easter_egg', methods=['GET', 'POST'])
# def easteregg():
#     if request.method == 'POST':
#         egg = request.form.get['egg']
        
#         if egg == 'cow':
#             return cowsay()
#         elif egg == 'fortune':
#             return fortune()
#     else:
#         return redirect('/')

# def cowsay():
#     # ランダムにキャラクターを選択
#     charactor = variable.cowsayCharacters[random.randint(0, len(variable.cowsayCharacters) - 1)]
#     # 台詞をランダムに選択
#     message = variable.cowsayMessage[random.randint(0, len(variable.cowsayMessage) - 1)]
#     # cowsayコマンドを実行
#     result = subprocess.run(['/usr/games/cowsay', '-f', charactor, message], encoding='utf-8', stdout=subprocess.PIPE)
#     # 連続する空白を&nbsp;に置換
#     formatted_text = re.sub(r' {2,}', lambda match: '&nbsp;' * len(match.group()), result.stdout)
#     # 改行を<br>タグに置換
#     formatted_text = formatted_text.replace('\n', '<br>')
#     # 置換したテキストをHTMLに渡す
#     return render_template('out.html', text=formatted_text)

# def fortune():
#     return render_template('out.html', text=variable.fortuneList[random.randint(0, len(variable.fortuneList) - 1)])