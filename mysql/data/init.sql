-- drop table if exists ranking;
-- -- 匿名でランキングに登録するためのテーブル。適当に作成したテーブルなので適宜変更しましょう。
-- create table ranking (
--     id int primary key auto_increment,
--     name varchar(255) NOT NULL,
--     score int NOT NULL,
--     picture varchar(255)
-- );

-- INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人１', 8);
-- INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人２', 7);
-- INSERT INTO ranking (name, score) VALUES ('名無しの弁当職人３', 6);
-- INSERT INTO ranking (name, score) VALUES ('さすらいの料理人', 15);

drop table if exists colors;
-- 使う色のテーブル
CREATE TABLE colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO colors (name) VALUES 
    ('red'),
    ('yellow'),
    ('green'),
    ('white'),
    ('black'),
    ('brown'),
    ('blue'),
    ('gray'),
    ('green-blue'),
    ('light-blue'),
    ('purple');

-- drop table if exists foods;
-- -- 色ごとの食材テーブル
-- CREATE TABLE foods (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     color varchar(255) NOT NULL,
--     nutrient varchar(255) NOT NULL,
--     point INT DEFAULT 0,
--     FOREIGN KEY (color) REFERENCES colors(name),
--     FOREIGN KEY (nutrient) REFERENCES nutrients(name)
-- );
-- -- nutrientsは栄養素を表す。現在は仮でprotein,carb,fat,vitamin,mineralsの5つを用意しているが、値は適当なので要変更。

-- INSERT INTO foods (name, color, nutrient) VALUES 
-- -- 食材
-- -- 赤
-- ('トマト', 'red', 'vitamin'),
-- ('パプリカ（赤）', 'red', 'vitamin'),
-- ('イチゴ', 'red', 'vitamin'),
-- ('リンゴ', 'red', 'vitamin'),
-- ('スモモ', 'red', 'vitamin'),
-- ('赤ピーマン', 'red', 'vitamin'),
-- ('サーモン', 'red', 'fat'),
-- ('カプレーゼ', 'red', 'protein'),
-- ('チェリートマト', 'red', 'vitamin'),
-- ('赤ぶどう', 'red', 'vitamin'),
-- ('梅干し', 'red', 'vitamin'),
-- ('赤リンゴ', 'red', 'vitamin'),
-- ('ローストビーフ', 'red', 'protein'),
-- ('ハム', 'red', 'protein'),
-- ('焼き鮭', 'red', 'protein'),

-- ('トマト', 'red', 'vitamin'),
-- ('イチゴ', 'red', 'vitamin'),
-- ('リンゴ', 'red', 'vitamin'),
-- ('梅干し', 'red', 'vitamin'),
-- ('ハム', 'red', 'vitamin'),

-- -- 黄
-- ('ニンジン', 'yellow', 'vitamin'),
-- ('カボチャ', 'yellow', 'vitamin'),
-- ('みかん', 'yellow', 'vitamin'),
-- ('パパイヤ', 'yellow', 'vitamin'),
-- ('クルミ', 'yellow', 'fat'),
-- ('コーン', 'yellow', 'vitamin'),
-- ('パプリカ（黄）', 'yellow', 'vitamin'),
-- ('マンゴー', 'yellow', 'vitamin'),
-- ('バナナ', 'yellow', 'carb'),
-- ('パイナップル', 'yellow', 'vitamin'),
-- ('レモン', 'yellow', 'vitamin'),
-- ('かぼちゃ', 'yellow', 'vitamin'),
-- ('生姜', 'yellow', 'vitamin'),
-- ('卵焼き', 'yellow', 'protein'),
-- ('たくあん', 'yellow', 'vitamin'),
-- ('フライドチキン', 'yellow', 'protein'),
-- ('ツナサラダ', 'yellow', 'protein'),


-- ('コーン', 'yellow', 'vitamin'),
-- ('バナナ', 'yellow', 'vitamin'),
-- ('パイナップル', 'yellow', 'vitamin'),
-- ('卵焼き', 'yellow', 'vitamin'),
-- ('たくあん', 'yellow', 'vitamin'),

-- -- 緑
-- ('ほうれん草', 'green', 'vitamin'),
-- ('ブロッコリー', 'green', 'vitamin'),
-- ('枝豆', 'green', 'protein'),
-- ('グリーンピース', 'green', 'vitamin'),
-- ('レタス', 'green', 'vitamin'),
-- ('キウイ', 'green', 'vitamin'),
-- ('ピーマン', 'green', 'vitamin'),
-- ('アボカド', 'green', 'fat'),
-- ('グリーンアップル', 'green', 'vitamin'),
-- ('ズッキーニ', 'green', 'vitamin'),
-- ('ケール', 'green', 'vitamin'),
-- ('スプラウト', 'green', 'vitamin'),
-- ('小松菜', 'green', 'vitamin'),
-- ('しそ', 'green', 'vitamin'),
-- ('エンドウ豆', 'green', 'protein'),
-- ('アスパラガス', 'green', 'vitamin'),
-- ('パセリ', 'green', 'vitamin'),
-- ('青じそ', 'green', 'vitamin'),
-- ('ほうれん草のごま和え', 'green', 'vitamin'),
-- ('白菜', 'green', 'vitamin'),

-- ('ほうれん草', 'green', 'vitamin'),
-- ('ブロッコリー', 'green', 'vitamin'),-- light-green
-- ('枝豆', 'green', 'vitamin'),-- yellow-green
-- ('グリーンピース', 'green', 'vitamin'),-- yellow-green
-- ('レタス', 'green', 'vitamin'),-- light-green
-- ('ピーマン', 'green', 'vitamin'),-- light-green
-- ('小松菜', 'green', 'vitamin'),-- green-blue
-- ('エンドウ豆', 'green', 'vitamin'),
-- ('アスパラガス', 'green', 'vitamin'),
-- ('パセリ', 'green', 'vitamin'),

-- -- 白
-- ('ごはん', 'white', 'carb'),
-- ('大根', 'white', 'vitamin'),
-- ('豆腐', 'white', 'protein'),
-- ('カリフラワー', 'white', 'vitamin'),
-- ('豆乳', 'white', 'protein'),
-- ('ヨーグルト', 'white', 'protein'),
-- ('チーズ', 'white', 'protein'),
-- ('マッシュルーム', 'white', 'vitamin'),
-- ('タケノコ', 'white', 'vitamin'),
-- ('カニカマサラダ', 'white', 'protein'),
-- ('ポテトサラダ', 'white', 'carb'),

-- ('大根', 'white', 'carb'),
-- ('タケノコ', 'white', 'carb'),
-- ('ポテトサラダ', 'white', 'carb'),

-- -- 黒
-- ('ひじき', 'black', 'minerals'),
-- ('黒豆', 'black', 'protein'),
-- ('黒ごま', 'black', 'minerals'),
-- ('黒米', 'black', 'carb'),
-- ('海苔', 'black', 'vitamin'),
-- ('なす', 'black', 'vitamin'),
-- ('紫キャベツ', 'black', 'vitamin'),
-- ('さつまいもの煮物', 'black', 'carb'),
-- ('紫芋', 'black', 'vitamin'),

-- ('ひじき', 'black', 'vitamin'),
-- ('黒豆', 'black', 'vitamin'),
-- ('海苔', 'black', 'vitamin'),


-- -- 茶
-- ('こんにゃく', 'brown', 'vitamin'),
-- ('さつまいも', 'brown', 'carb'),
-- ('玄米', 'brown', 'carb'),
-- ('紅茶', 'brown', 'vitamin'),
-- ('ナッツ', 'brown', 'fat'),
-- ('チョコレート', 'brown', 'fat'),
-- ('コーヒー', 'brown', 'minerals'),
-- ('しいたけ', 'brown', 'vitamin'),
-- ('クルミ', 'brown', 'fat'),
-- ('オートミール', 'brown', 'carb'),
-- ('アーモンド', 'brown', 'fat'),
-- ('ハンバーグ', 'brown', 'protein'),
-- ('筑前煮', 'brown', 'carb'),
-- ('照り焼きチキン', 'brown', 'protein'),
-- ('春巻き', 'brown', 'carb'),
-- ('エビフライ', 'brown', 'protein'),
-- ('鶏の唐揚げ', 'brown', 'protein'),
-- ('チキン南蛮', 'brown', 'protein'),


-- ('さつまいも', 'brown', 'protein'),
-- ('しいたけ', 'brown', 'protein'),
-- ('ハンバーグ', 'brown', 'protein'),
-- ('筑前煮', 'brown', 'protein'),
-- ('照り焼きチキン', 'brown', 'protein'),
-- ('春巻き', 'brown', 'protein'),
-- ('エビフライ', 'brown', 'protein'),
-- ('鶏の唐揚げ', 'brown', 'protein'),
-- ('エビフライ', 'brown', 'protein'),

-- -- 青
-- ('ブルーベリー', 'blue', 'vitamin'),

-- -- 灰
-- ('黒ごま', 'gray', 'minerals'),
-- ('灰もち米', 'gray', 'carb'),
-- ('レンコンきんぴら', 'gray', 'carb'),
-- ('煮しめ', 'gray', 'carb'),

-- -- 料理名
-- -- geminiで判断された場合色を加点するために判断されにくいご飯を追加
-- ('米', 'white', 'protein'),
-- ('牛丼', 'brown', 'carb'),
-- ('日の丸弁当', 'red', 'protein'),
-- ('ハム', 'red', 'protein'),
-- ('そぼろ', 'yellow', 'protein'),
-- ('そぼろ', 'brown', 'protein'),
-- ('そぼろ', 'green', 'protein'),
-- ('焼きそば', 'brown', 'protein'),
-- ('サンドイッチ', 'red', 'protein'),
-- ('サンドイッチ', 'green', 'protein'),
-- ('サンドイッチ', 'brown', 'protein'),
-- ('オムライス', 'yellow', 'carb');

drop table if exists test;
create table test (
    id int primary key auto_increment,
    name varchar(255) not null,
    value text,
    created_date timestamp default current_timestamp,
    updated_date timestamp default current_timestamp on update current_timestamp
);

INSERT INTO test (name, value) VALUES ('test1', 'テストデータを入力しましたm(_ _)m');

drop table if exists users;
-- ユーザーテーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(1024) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, password, email) VALUES
    ('管理者', 'scrypt:32768:8:1$XjdE0om2F6R5BEDA$26011fc04d5619203454e207a38455a80d6b219819b556d4544b7a3aabb9b7aa8133cc5e4d5112878c5c439c83f1dba29f53d651794d1e461f3366397ec7f0f2', 'args@vvv.ok'),
    ('匿名ユーザー', 'scrypt:32768:8:1$vWYcyi9nQNFQYrjS$f5fdd73d4f53207b9f5e9e8e605c09dda987df71ee4d5fd4aea17d141eb2b6a32e7d9340e8a2b4716bbf36b154a6f309e921011a4a8f7e9286c7f2c2a8065eae', 'hoge@test.com'),
    ('テストユーザー', 'scrypt:32768:8:1$vWYcyi9nQNFQYrjS$f5fdd73d4f53207b9f5e9e8e605c09dda987df71ee4d5fd4aea17d141eb2b6a32e7d9340e8a2b4716bbf36b154a6f309e921011a4a8f7e9286c7f2c2a8065eae', 'test@test.com');

drop table if exists lunch_score;
-- スコアテーブル
-- "is_not_lunch"がtrueの場合は写真内に弁当が含まれていないと判断されたことを意味する
CREATE TABLE lunch_score (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    lunch_image_name VARCHAR(255) NOT NULL,
    use_gemini BOOLEAN DEFAULT TRUE,
    is_not_lunch BOOLEAN DEFAULT FALSE,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    all_result text,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

drop table if exists lunch_comment;
-- 各色に対するコメントのテーブル
-- "is_positive"がtrue：大まかな採点理由を肯定的に書いたもの
--              　false：改善することで得点が高くなる可能性を書いたもの
CREATE TABLE lunch_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    color VARCHAR(255) NOT NULL,
    is_positive BOOLEAN DEFAULT TRUE,
    comment TEXT NOT NULL
);

INSERT INTO lunch_comment (color, is_positive, comment) VALUES
    ('red', TRUE, '赤色は、交感神経を刺激し、代謝を活発にする効果があります。これにより、<br>食欲が増進され、食事の際の満足度も高まる傾向にあります。'),
    ('red', TRUE, '赤色は、情熱や興奮、高揚感を引き起こす色として知られています。<br>お弁当に赤色を取り入れることで、食べる人に活力を与え、気分を高揚させることができます。'),
    ('red', TRUE, '赤色は、視覚的に非常に目立つ色なので、お弁当の中で他の色を引き立て、注意を引きつける効果があります。'),
    ('yellow', TRUE, '黄色は視覚的に美味しそうであったり食欲をそそるといったイメージを持ちやすいです。<br>また、ポジティブな印象を与えることが多いです。<br>これらは食べたいという感情に繋がるだけでなく、盛り付けた際の印象が良くなり、お弁当がより魅力的になります。'),
    ('brown', TRUE, '茶色は肉、揚げ物等の美味しいと感じる傾向にある物が連想されやすい色です。<br>そのため食欲を増加させるのに効果的な色です。'),
    ('red', FALSE, '暖色系の色は食べ物のうま味を強調し、料理の見栄えを良くします。<br>また、美味しそうな印象を与える効果があり、より良いお弁当になります。'),
    ('yellow', FALSE, '暖色系の色は食べ物のうま味を強調し、料理の見栄えを良くします。<br>また、美味しそうな印象を与える効果があり、より良いお弁当になります。'),
    ('green', FALSE, 'もう少し緑野菜を増やすと良いでしょう。<br>野菜は視覚的にも美しく、栄養価も高いため、バランスの良いお弁当になります。'),

    -- 以下はAIによる仮のコメント
    ('yellow', TRUE, '黄色は、太陽の色であり、明るく元気なイメージを持つ色です。<br>お弁当に黄色を取り入れることで、食べる人に活力を与え、気分を高揚させることができます。'),
    ('yellow', TRUE, '黄色は、食欲を増進させる効果があると言われています。<br>お弁当に黄色を取り入れることで、食べる人の食欲を増進させることができます。'),
    ('green', TRUE, '緑色は、安らぎや安心感を与える効果があります。<br>また、緑色は、自然との調和や健康をイメージさせる色としても知られています。<br>お弁当に緑色を取り入れることで、食べる人に安らぎや安心感を与えることができます。'),
    ('green', TRUE, '緑色は、リラックス効果があると言われています。<br>お弁当に緑色を取り入れることで、食べる人のリラックス効果を高めることができます。'),
    ('green', TRUE, '緑色は、目に優しい色として知られています。<br>お弁当に緑色を取り入れることで、食べる人の目に優しい印象を与えることができます。'),
    ('white', TRUE, '白色は、清潔感や無垢さをイメージさせる効果があります。<br>また、白色は、シンプルで上品な印象を与える色としても知られています。');