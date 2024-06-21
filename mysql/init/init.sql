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

-- 色ごとの食材テーブル
CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    color ENUM('赤','黒赤','白赤','橙','黒橙','白橙','黄','黒黄','白黄',
    '緑','黒緑','白緑','青','黒青','白青','紫','黒紫','白紫','黒','白','灰','茶') NOT NULL,
    nutrients ENUM('protein','carb','fat','vitamin','minerals') NOT NULL
);

INSERT INTO ingredients (name, description, color,nutrients) VALUES 
('トマト', 'ビタミンCが豊富な野菜', '赤', 'vitamin'),
('パプリカ（赤）', 'カプサイシンを含む野菜', '赤', 'vitamin'),
('ほうれん草', '鉄分が豊富な葉物野菜', '緑', 'vitamin'),
('ブロッコリー', 'ビタミンKが豊富な野菜', '緑', 'vitamin'),
('コーン', '甘くておいしい野菜', '黄', 'vitamin'),
('パプリカ（黄）', 'ビタミンCが豊富な野菜', '黄', 'vitamin'),
('ごはん', '日本のお弁当の主食', '白', 'vitamin'),
('大根', '消化を助ける根菜', '白', 'vitamin'),
('ひじき', '鉄分が豊富な海藻', '黒', 'vitamin'),
('黒豆', 'タンパク質が豊富な豆類', '黒', 'vitamin');

-- 赤
('トマト', 'ビタミンCが豊富な野菜', '赤', 'vitamin'),
('パプリカ（赤）', 'カプサイシンを含む野菜', '赤', 'vitamin'),
-- 黒赤
('チェリートマト', 'ミニサイズの赤いトマト', '黒赤', 'vitamin'),
-- 白赤
('白パプリカ（赤）', '白色のパプリカで中は赤', '白赤', 'vitamin'),
-- 橙
('ニンジン', 'ベータカロテンが豊富な野菜', '橙', 'vitamin'),
-- 黒橙
('黒ニンジン', '黒色の皮を持つニンジン', '黒橙', 'vitamin'),
-- 白橙
('白人参', '白色の人参', '白橙', 'vitamin'),
-- 黄
('コーン', '甘くておいしい野菜', '黄', 'vitamin'),
('パプリカ（黄）', 'ビタミンCが豊富な野菜', '黄', 'vitamin'),
-- 黒黄
('黒パプリカ（黄）', '黒色の皮を持つ黄色のパプリカ', '黒黄', 'vitamin'),
-- 白黄
('白カボチャ', '白色の皮を持つカボチャ', '白黄', 'vitamin'),
-- 緑
('ほうれん草', '鉄分が豊富な葉物野菜', '緑', 'vitamin'),
('ブロッコリー', 'ビタミンKが豊富な野菜', '緑', 'vitamin'),
-- 黒緑
('ケール（黒）', '黒色の葉を持つケール', '黒緑', 'vitamin'),
-- 白緑
('白ほうれん草', '白色の茎を持つほうれん草', '白緑', 'vitamin'),
-- 青
('青じそ', '香りが良い葉', '青', 'vitamin'),
-- 黒青
('黒紫蘇', '黒色の紫蘇', '黒青', 'vitamin'),
-- 白青
('白紫蘇', '白色の紫蘇', '白青', 'vitamin'),
-- 紫
('なす', 'ナスニンを含む紫の野菜', '紫', 'vitamin'),
-- 黒紫
('黒ナス', '黒色のナス', '黒紫', 'vitamin'),
-- 白紫
('白ナス', '白色のナス', '白紫', 'vitamin'),
-- 黒
('ひじき', '鉄分が豊富な海藻', '黒', 'vitamin'),
('黒豆', 'タンパク質が豊富な豆類', '黒', 'vitamin'),
-- 白
('ごはん', '日本のお弁当の主食', '白', 'vitamin'),
('大根', '消化を助ける根菜', '白', 'vitamin'),
-- 灰
('黒ごま', 'カルシウムが豊富な種子', '灰', 'vitamin'),
-- 茶
('こんにゃく', '低カロリー食品', '茶', 'vitamin');