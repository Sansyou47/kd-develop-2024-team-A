drop table if exists ranking;
-- 匿名でランキングに登録するためのテーブル。適当に作成したテーブルなので適宜変更しましょう。
create table ranking (
    rank_ID int primary key auto_increment,
    name varchar(255) not null,
    score int not null,
    picture varchar(255)
);

INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人１', 8);
INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人２', 7);
INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人３', 6);
INSERT INTO ranking (name, score) VALUES ('さすらいの料理人', 15);

drop table if exists colors;
-- 使う色のテーブル
CREATE TABLE colors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO colors (name) VALUES
('赤'),
('黒赤'),
('白赤'),
('橙'),
('黒橙'),
('白橙'),
('黄'),
('黒黄'),
('白黄'),
('緑'),
('黒緑'),
('白緑'),
('青'),
('黒青'),
('白青'),
('紫'),
('黒紫'),
('白紫'),
('黒'),
('白'),
('灰'),
('茶');

drop table if exists foods;
-- 色ごとの食材テーブル
CREATE TABLE foods (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    color ENUM('red','yellow','green','white','black','brown','blue','gray','green-blue','light-blue','purple') NOT NULL,
    nutrients ENUM('protein','carb','fat','vitamin','minerals') NOT NULL,
    point INT DEFAULT 0
);
-- nutrientsは栄養素を表す。現在は仮でprotein,carb,fat,vitamin,mineralsの5つを用意しているが、値は適当なので要変更。

INSERT INTO foods (name, color, nutrients) VALUES 
-- 食材
-- 赤
('トマト', 'red', 'vitamin'),
('パプリカ（赤）', 'red', 'vitamin'),
('イチゴ', 'red', 'vitamin'),
('リンゴ', 'red', 'vitamin'),
('スモモ', 'red', 'vitamin'),
('赤ピーマン', 'red', 'vitamin'),
('サーモン', 'red', 'fat'),
('カプレーゼ', 'red', 'protein'),
('チェリートマト', 'red', 'vitamin'),
('赤ぶどう', 'red', 'vitamin'),
('梅干し', 'red', 'vitamin'),
('赤リンゴ', 'red', 'vitamin'),
('ローストビーフ', 'red', 'protein'),
('ハム', 'red', 'protein'),
('焼き鮭', 'red', 'protein'),

-- 黄
('ニンジン', 'yellow', 'vitamin'),
('カボチャ', 'yellow', 'vitamin'),
('みかん', 'yellow', 'vitamin'),
('パパイヤ', 'yellow', 'vitamin'),
('クルミ', 'yellow', 'fat'),
('コーン', 'yellow', 'vitamin'),
('パプリカ（黄）', 'yellow', 'vitamin'),
('マンゴー', 'yellow', 'vitamin'),
('バナナ', 'yellow', 'carb'),
('パイナップル', 'yellow', 'vitamin'),
('レモン', 'yellow', 'vitamin'),
('かぼちゃ', 'yellow', 'vitamin'),
('生姜', 'yellow', 'vitamin'),
('卵焼き', 'yellow', 'protein'),
('たくあん', 'yellow', 'vitamin'),
('フライドチキン', 'yellow', 'protein'),
('ツナサラダ', 'yellow', 'protein'),

-- 緑
('ほうれん草', 'green', 'vitamin'),
('ブロッコリー', 'green', 'vitamin'),
('枝豆', 'green', 'protein'),
('グリーンピース', 'green', 'vitamin'),
('レタス', 'green', 'vitamin'),
('キウイ', 'green', 'vitamin'),
('ピーマン', 'green', 'vitamin'),
('アボカド', 'green', 'fat'),
('グリーンアップル', 'green', 'vitamin'),
('ズッキーニ', 'green', 'vitamin'),
('ケール', 'green', 'vitamin'),
('スプラウト', 'green', 'vitamin'),
('小松菜', 'green', 'vitamin'),
('しそ', 'green', 'vitamin'),
('エンドウ豆', 'green', 'protein'),
('アスパラガス', 'green', 'vitamin'),
('パセリ', 'green', 'vitamin'),
('青じそ', 'green', 'vitamin'),
('ほうれん草のごま和え', 'green', 'vitamin'),
('白菜', 'green', 'vitamin'),

-- 白
('ごはん', 'white', 'carb'),
('大根', 'white', 'vitamin'),
('豆腐', 'white', 'protein'),
('カリフラワー', 'white', 'vitamin'),
('豆乳', 'white', 'protein'),
('ヨーグルト', 'white', 'protein'),
('チーズ', 'white', 'protein'),
('マッシュルーム', 'white', 'vitamin'),
('タケノコ', 'white', 'vitamin'),
('カニカマサラダ', 'white', 'protein'),
('ポテトサラダ', 'white', 'carb'),

-- 黒
('ひじき', 'black', 'minerals'),
('黒豆', 'black', 'protein'),
('黒ごま', 'black', 'minerals'),
('黒米', 'black', 'carb'),
('海苔', 'black', 'vitamin'),
('なす', 'black', 'vitamin'),
('紫キャベツ', 'black', 'vitamin'),
('さつまいもの煮物', 'black', 'carb'),
('紫芋', 'black', 'vitamin'),

-- 茶
('こんにゃく', 'brown', 'vitamin'),
('さつまいも', 'brown', 'carb'),
('玄米', 'brown', 'carb'),
('紅茶', 'brown', 'vitamin'),
('ナッツ', 'brown', 'fat'),
('チョコレート', 'brown', 'fat'),
('コーヒー', 'brown', 'minerals'),
('しいたけ', 'brown', 'vitamin'),
('クルミ', 'brown', 'fat'),
('オートミール', 'brown', 'carb'),
('アーモンド', 'brown', 'fat'),
('ハンバーグ', 'brown', 'protein'),
('筑前煮', 'brown', 'carb'),
('照り焼きチキン', 'brown', 'protein'),
('春巻き', 'brown', 'carb'),
('エビフライ', 'brown', 'protein'),
('鶏の唐揚げ', 'brown', 'protein'),
('チキン南蛮', 'brown', 'protein'),

-- 青
('ブルーベリー', 'blue', 'vitamin'),

-- 灰
('黒ごま', 'gray', 'minerals'),
('灰もち米', 'gray', 'carb'),
('レンコンきんぴら', 'gray', 'carb'),
('煮しめ', 'gray', 'carb'),

-- 料理名
-- geminiで判断された場合色を加点するために判断されにくいご飯を追加
('米', 'white', 'protein'),
('牛丼', 'brown', 'carb'),
('日の丸弁当', 'red', 'protein'),
('ハム', 'red', 'protein'),
('そぼろ', 'yellow', 'protein'),
('そぼろ', 'brown', 'protein'),
('そぼろ', 'green', 'protein'),
('焼きそば', 'brown', 'protein'),
('サンドイッチ', 'red', 'protein'),
('サンドイッチ', 'green', 'protein'),
('サンドイッチ', 'brown', 'protein'),
('オムライス', 'yellow', 'carb');

drop table if exists test;
create table test (
    id int primary key auto_increment,
    name varchar(255) not null
);

INSERT INTO test (name) VALUES ('test1');