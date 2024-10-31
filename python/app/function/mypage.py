from flask import Blueprint, render_template, request, redirect,session
from function import mysql
import base64, os
import json

#やってること
#まずログインチェックを行う
#してるなら弁当点数履歴確認に必要な情報をDBから渡す
#戻り値はlunch_score
#画像ファイルから対応する画像を持ってくる
#してないならログイン画面に飛ばす


# Blueprintの登録（名前はファイル名が定例）
app = Blueprint("mypage", __name__)
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if "user_id" in session:
        user_id = session["user_id"]
        # 30日間セッションを保持
        session.permanent = True
        # 空の変数を用意
        id = None               # ID
        score = None            # 点数
        token_point = None     #点数詳細
        image_name = None       # 画像名
        create_date = None      # 日付
        mypage_data_size = 0    # ページング用の変数
  # ソート用の変数 POSTがない場合はNone
        page = int(request.form.get('page') or request.args.get('page', 1))
        sort_type = request.form.get('sort_type') or request.args.get('sort_type', 'date')
        sort_direction = request.form.get('sort_direction') or request.args.get('sort_direction', 'desc')
        # if request.method == 'POST':
        #     sort_type = request.form['sort_type']
        #     sort_direction = request.form['sort_direction']
        # else:
        #     sort_type = "date"
        #     sort_direction = "desc"

        
        # エラーメッセージ
        title = 'Oops！エラーが発生しちゃった！😭'
        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'

        # ログインしているIDをセッションから取得
        # try:
            # URLクエリからsort_typeを取得
            # sort_type = request.args.get('sort_type', 'date')
            # direction = request.args.get('direction', 'desc')
            # # もしPOSTでsort_type(日付or点数)が送られてきたら
            # if request.method == 'POST':
            #     # フォームから送られてきたsort_typeを取得
            #     sort_type = request.form['sort_type']
            #     # いつか使うかも フォームから送られてきたsort_typeをセッションに保存
            #     # session['sort_type'] = sort_type
            # # URLクエリからsort_direction(昇順or降順)を取得
            # if request.method == 'POST':
            #     # フォームから送られてきたdirectionを取得
            #     sort_direction = request.form['sort_direction']
            #     # いつか使うかも フォームから送られてきたdirectionをセッションに保存
            #     # session['sort_direction'] = sort_direction

            # # # もしsort_typeが空だったら
            # # if sort_type == None:
            # #     # sort_typeに初期値を代入
            # #     sort_type = 'date'
            # # # もしsort_directionが空だったら
            # # if sort_direction == None:
            # #     # sort_directionに初期値を代入
            # #     sort_direction = 'desc'

        # sql変数の初期化
        sql = 'SELECT id, score, token_point,lunch_image_name, create_date FROM lunch_score WHERE user_id = %s ORDER BY create_date DESC'
        # sort_typeがdateのとき SQL文で日付の降順でデータを取得
        if sort_type == 'date':
            # sort_directionがdescのとき SQL文で日付の降順でデータを取得
            if sort_direction == 'desc':
                sql = 'SELECT id, score, token_point,lunch_image_name, create_date FROM lunch_score WHERE user_id = %s ORDER BY create_date DESC'   
            # sort_directionがascのとき SQL文で日付の昇順でデータを取得
            else:
                sql = 'SELECT id, score, token_point,lunch_image_name, create_date FROM lunch_score WHERE user_id = %s ORDER BY create_date ASC'   
        # sort_typeがscoreのとき SQL文で点数の降順でデータを取得
        elif sort_type == 'score':
            # sort_directionがdescのとき SQL文で点数の降順でデータを取得
            if sort_direction == 'desc':
                sql = 'SELECT id, score, token_point,lunch_image_name, create_date FROM lunch_score WHERE user_id = %s ORDER BY score DESC'
            # sort_directionがascのとき SQL文で点数の昇順でデータを取得
            else:
                sql = 'SELECT id, score, token_point,lunch_image_name, create_date FROM lunch_score WHERE user_id = %s ORDER BY score ASC'
        # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
        mysql.cur.execute(sql, (user_id,))
        # resultに入れる
        result = mysql.cur.fetchall()
        # 画像を読み込み
        mypage_result_zen = []
        for row in result:
            id = row[0]             # 0番目のデータのIDを取得
            score = row[1]          # 1番目のデータの点数を取得
            token_point = row[2]   # 2番目のデータの点数詳細を取得 高木君の画面にだすやつ
            image_name = row[3]     # 3番目のデータの画像名を取得
            create_date = row[4]    # 4番目のデータの日付を取得

            # 相対パスを使用して画像パスを指定
            image_path = os.path.join(os.path.dirname(__file__),'..','rmbg', 'original', f'{image_name}.jpeg')
            # try:
            with open(image_path, "rb") as image:
                # 画像を読み込みbase64にエンコード
                image_data = image.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                # 画像をdataURIに変換
                bento_url = f"data:image/jpeg;base64,{encoded_image}"
                mypage_result_zen.append((id, score, token_point, bento_url, create_date))
    #         except Exception as e:
    #             title = 'Oops！エラーが発生しちゃった！😭'
    #             message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
    #             return render_template('error.html', title=title, message=message, error=e)
    # except Exception as e:
    #         return render_template('error.html', title=title, message=message, error=e)

        # ページングに関する処理
        # paging_numにmypage_result_zenの長さを入れる
        mypage_data_size = len(mypage_result_zen)

        # POSTでpageが送られなかったら
        # POSTのときフォームから、GETのときURLパラメータから取得
        # page = int(request.form.get('page') or request.args.get('page', 1))
        # page = int(request.args.get('page',1))
        page_contents = 5    # 1ページに表示する数
        start = (page - 1) * page_contents
        end = start + page_contents
        mypage_result_page = mypage_result_zen[start:end]

        # lunch_scoreの情報をmypage.htmlに渡す
        return render_template('mypage.html', mypage_result_zen=mypage_result_page,
                               user_id=user_id, mypage_data_size=mypage_data_size,page=page,
                               page_contents=page_contents,sort_type=sort_type,sort_direction=sort_direction)
    else:
        return redirect('/login')


#やろうとしたこと
#マイページの個別弁当の個別の詳細表示
#ポップアップされた詳細結果から右下の詳細表示ボタンを押すと、その弁当の詳細結果(結果画面)が表示される
#パス表示(URL)を/mypage/logにして、render_template('image_result.html')を受け取っている

@app.route('/mypage/log', methods=['GET', 'POST'])
def bento_log():
    id = None               # ID
    score = None            # 点数
    token_point = None     #点数詳細
    all_result = None          #詳細ページの全ての変数
    bento_url = None        # 画像URL
    #########明日の俺へsqlのwhereをid(socre_lunch)にすれば行けそうそれと、嫁坂が変な顔したら橋本君がテーブル作りますｷｭﾋﾟ#########
    if request.method == 'POST':       
        try:
            #POSTで送られてきたidを取得
            id = request.form["id"]
            score = request.form["score"]
            token_point = request.form["token_point"]
            bento_url = request.form["bento_url"]
            # SQL文で対象のデータを取得
            sql = 'SELECT all_result FROM lunch_score WHERE id = %s'   
            # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute(sql, (id,))
            # resultに入れる
            result = mysql.cur.fetchall()
            for row in result:
                all_result = row[0]     # 1番目のデータの点数を取得
                # JSON形式の文字列をリストに変換
                all_result = json.loads(all_result)
                
                # all_resultを個々の変数に分割
                color_point = all_result[0]
                color_point_name_code = all_result[1]
                color_point_name_jp = all_result[2]
                colors_code = all_result[3]
                colors_per = all_result[4]
                color_graph = all_result[5]
                nakai_color_zen = all_result[6]
                #gemini_responseをresposeで最後返すdemoの150行基準
                gemini_response = all_result[7]
                Shortage_result = all_result[8]


            # lunch_scoreの情報をmypage.htmlに渡す
            return render_template('image_result.html',id=id, color_score_inc=score,token_point=token_point, data_uri=bento_url,color_point=color_point,color_point_name_code=color_point_name_code,color_point_name_jp=color_point_name_jp,colors_code=colors_code,colors_per=colors_per,color_graph=color_graph,nakai_color_zen=nakai_color_zen,response=gemini_response,Shortage_result=Shortage_result)
            
        except Exception as e:
            title = 'Oops！エラーが発生しちゃった！😭'
            message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
            return render_template('error.html', title=title, message=message, error=e)
    else:
        return redirect('/login')
