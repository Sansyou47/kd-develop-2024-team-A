from flask import Blueprint, render_template, request, redirect,session
from function import mysql, login
import base64, os,datetime
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
        #ログインチェック
        #引数はログイン後に行きたいurl
        #引数無しの場合はルートに返す
        login_check = login.check('/mypage')
        if login_check:
            return login_check
        
        user_id = session['user_id']
        # 空の変数を用意
        id = None               # ID
        score = None            # 点数
        image_name = None       # 画像名
        create_date = None      # 日付
        sum_score = 0           # 点数の合計
        avg_score = None        # 平均点数
        max_score = 0           # 最高点数
        mypage_data_size = 0    # ページング用の変数
        # ソート用の変数 POSTがない場合はNone
        page = int(request.form.get('page') or request.args.get('page', 1))
        sort_type = request.form.get('sort_type') or request.args.get('sort_type', 'date')
        sort_direction = request.form.get('sort_direction') or request.args.get('sort_direction', 'desc')
        filter_point = request.form.get('filter_point') or request.args.get('filter_point', 'all')
        filter_point_start = request.form.get('filter_point_start') or request.args.get('filter_point_start', 0)
        filter_point_end = request.form.get('filter_point_end') or request.args.get('filter_point_end', 100)
        filter_date_start = request.form.get('filter_date_start') or request.args.get('filter_date_start', '')
        filter_date_end = request.form.get('filter_date_end') or request.args.get('filter_date_end', '')
        date_start = ""
        date_end = ""
        # もしfilter_date_startが空の場合は1990-01-01を代入
        if filter_date_start == '':
            date_start = '1990-01-01 00:00:00'
        else:
            date_start = filter_date_start
            date_start = filter_date_start + ' 00:00:00'
        # もしfilter_date_endが空の場合は本日の日付を代入
        if filter_date_end == '':
            date_end = '2999-12-31 23:59:59'
        else:
            date_end = filter_date_end
            date_end = filter_date_end + ' 23:59:59'

        
        # エラーメッセージ
        title = 'Oops！エラーが発生しちゃった！😭'
        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'

        # ログインしているIDをセッションから取得
        try:
            # sql変数の初期化
            # "score >= %s AND score <= %s"で指定した点数範囲のデータを取得
            sql = 'SELECT id, score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s AND score >= %s AND score <= %s AND create_date BETWEEN %s AND %s ORDER BY create_date DESC'
            # sort_typeがdateのとき SQL文で日付の降順でデータを取得
            if sort_type == 'date':
                # sort_directionがdescのとき SQL文で日付の降順でデータを取得
                if sort_direction == 'desc':
                    sql = 'SELECT id, score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s AND score BETWEEN %s AND %s AND create_date BETWEEN %s AND %s ORDER BY create_date DESC'
                # sort_directionがascのとき SQL文で日付の昇順でデータを取得
                else:
                    sql = 'SELECT id, score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s AND score BETWEEN %s AND %s AND create_date BETWEEN %s AND %s ORDER BY create_date ASC'
            # sort_typeがscoreのとき SQL文で点数の降順でデータを取得
            elif sort_type == 'score':
                # sort_directionがdescのとき SQL文で点数の降順でデータを取得
                if sort_direction == 'desc':
                    sql = 'SELECT id, score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s AND score BETWEEN %s AND %s AND create_date BETWEEN %s AND %s ORDER BY score DESC'
                # sort_directionがascのとき SQL文で点数の昇順でデータを取得
                else:
                    sql = 'SELECT id, score, lunch_image_name, create_date FROM lunch_score WHERE user_id = %s AND score BETWEEN %s AND %s AND create_date BETWEEN %s AND %s ORDER BY score ASC'
            # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute(sql, (user_id,filter_point_start,filter_point_end,date_start,date_end))
            # resultに入れる
            result = mysql.cur.fetchall()
            
            # 今週の開始日と終了日を計算
            today = datetime.date.today()
            # start_of_week = today - datetime.timedelta(days=today.weekday())
            start_of_week = today
            end_of_week = start_of_week + datetime.timedelta(days=6)
            

            # 今週1週間の点数を取得するSQLクエリ
            sql_week = 'SELECT score FROM lunch_score WHERE user_id = %s AND create_date BETWEEN %s AND %s'
            mysql.cur.execute(sql_week, (user_id, start_of_week, end_of_week))
            result_week = mysql.cur.fetchall()

            # 平均点を計算
            if result_week:
                total_score_week = sum(row[0] for row in result_week)
                average_week = total_score_week / len(result_week)
                average_week = round(average_week, 0)
                max_week = max(row[0] for row in result_week)
                max_week = round(max_week, 0)
            else:
                average_week = 0
                max_week = 0
            
            # 画像を読み込み
            mypage_result_zen = []
            for row in result:
                id = row[0]             # 0番目のデータのIDを取得
                score = row[1]          # 1番目のデータの点数を取得
                image_name = row[2]     # 3番目のデータの画像名を取得
                create_date = row[3]    # 4番目のデータの日付を取得
                sum_score += score      # 点数の合計を計算
                if max_score < score:
                    max_score = score

                # 相対パスを使用して画像パスを指定
                image_path = os.path.join(os.path.dirname(__file__),'..','rmbg', 'original', f'{image_name}.jpeg')
                try:
                    with open(image_path, "rb") as image:
                        # 画像を読み込みbase64にエンコード
                        image_data = image.read()
                        encoded_image = base64.b64encode(image_data).decode('utf-8')
                        # 画像をdataURIに変換
                        bento_url = f"data:image/jpeg;base64,{encoded_image}"
                        mypage_result_zen.append((id, score, bento_url, create_date))
                except Exception as e:
                    if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                        return
                    else:
                        title = 'Oops！エラーが発生しちゃった！😭'
                        message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                        return render_template('error.html', title=title, message=message, error=e)
            # 平均点数を計算
            if sum_score != 0:
                avg_score = sum_score / len(result)
                avg_score = round(avg_score, 1)
            else:
                avg_score = 0
        except Exception as e:
            if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                return
            else:
                return render_template('error.html', title=title, message=message, error=e)

        # ページングに関する処理
        # paging_numにmypage_result_zenの長さを入れる
        mypage_data_size = len(mypage_result_zen)

        # POSTでpageが送られなかったら
        # POSTのときフォームから、GETのときURLパラメータから取得
        # page = int(request.form.get('page') or request.args.get('page', 1))
        # page = int(request.args.get('page',1))
        page_contents = 8    # 1ページに表示する数
        start = (page - 1) * page_contents
        end = start + page_contents
        mypage_result_page = mypage_result_zen[start:end]

                # lunch_scoreの情報をmypage.htmlに渡す
        return render_template('mypage.html', mypage_result_zen=mypage_result_page,
                                user_id=user_id, mypage_data_size=mypage_data_size,page=page,
                                page_contents=page_contents,
                                start_of_week=start_of_week,end_of_week=end_of_week,
                                avg_score=avg_score,max_score=max_score,average_week=average_week,max_week=max_week,
                                sort_type=sort_type,sort_direction=sort_direction,
                                filter_point=filter_point,filter_point_start=filter_point_start,filter_point_end=filter_point_end,
                                filter_date_start=filter_date_start,filter_date_end=filter_date_end)

#やろうとしたこと
#マイページの個別弁当の個別の詳細表示
#ポップアップされた詳細結果から右下の詳細表示ボタンを押すと、その弁当の詳細結果(結果画面)が表示される
#パス表示(URL)を/mypage/logにして、render_template('image_result.html')を受け取っている

@app.route('/mypage/log', methods=['GET', 'POST'])
def bento_log():
    id = None               # ID
    score = None            # 点数
    all_result = None          #詳細ページの全ての変数
    bento_url = None        # 画像URL
    #########明日の俺へsqlのwhereをid(socre_lunch)にすれば行けそうそれと、嫁坂が変な顔したら橋本君がテーブル作りますｷｭﾋﾟ#########
    if request.method == 'POST':       
        try:
            #POSTで送られてきたidを取得
            id = request.form["id"]
            # score = request.form["score"]
            bento_url = request.form["bento_url"]
            # SQL文で対象のデータを取得
            sql = 'SELECT score, all_result FROM lunch_score WHERE id = %s'   
            # 取得したIDを使ってデータベースにアクセスしてlunch_scoreの情報を取得
            mysql.cur.execute(sql, (id,))
            # resultに入れる
            result = mysql.cur.fetchone()
            
            if result:
                lunch_score = int(result[0])
                all_result = json.loads(result[1])
            
            color_point = all_result[0]
            color_point_name_code = all_result[1]
            color_point_name_jp = all_result[2]
            colors_code = all_result[3]
            colors_per = all_result[4]
            color_graph = all_result[5]
            nakai_color_zen = all_result[6]
            gemini_response = all_result[7]
            Shortage_result = all_result[8]
            
            # lunch_scoreの情報をimage_result.htmlに渡す
            return render_template('image_result.html',id=id, color_score_inc=lunch_score, data_uri=bento_url,color_point=color_point,color_point_name_code=color_point_name_code,color_point_name_jp=color_point_name_jp,colors_code=colors_code,colors_per=colors_per,color_graph=color_graph,nakai_color_zen=nakai_color_zen,response=gemini_response,Shortage_result=Shortage_result)
            
        except Exception as e:
            if session.get('user_id') == 1: # もし sessionのuser_idが管理者のとき エラー全文を返す
                return
            else:
                title = 'Oops！エラーが発生しちゃった！😭'
                message = 'アプリでエラーが起きちゃったみたい！申し訳ないけどもう一度やり直してね。'
                return render_template('error.html', title=title, message=message, error=e)
    else:
        return redirect('/login')