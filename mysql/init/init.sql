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