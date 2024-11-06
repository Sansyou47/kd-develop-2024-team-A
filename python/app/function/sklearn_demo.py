# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
import PIL
from PIL import Image
import cv2
import sklearn
from sklearn.cluster import KMeans
# Blueprintの登録（名前はファイル名が定例）
sk = Blueprint("sklearn_demo", __name__)

@sk.route('/sk')
def sk_demo():
    #画像を取り込む 画像のパスを指定する
    cv2_img = cv2.imread('./bento-haikeinashi.png')

    #RGBの並びに変換
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    #3次元配列を2次元配列に変換
    cv2_img = cv2_img.reshape(
    (cv2_img.shape[0] * cv2_img.shape[1], 3))

    print(cv2_img.shape)

    cluster = KMeans(n_clusters=10)

    cluster.fit(X=cv2_img)

    KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=10, n_init=10, random_state=None, tol=0.0001, verbose=0)

    # クラスタの中心座標を16進数に変換して返す
    cluster_centers_hex = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)) for r, g, b in cluster.cluster_centers_]
    for rgb_arr in cluster_centers_hex:
        color_img = Image.new(
            mode='RGB', size=(32,32), color=rgb_arr)

    return render_template("colorstest.html", colors=cluster_centers_hex)