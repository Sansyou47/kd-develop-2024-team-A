from PIL import Image

# 名前と年齢を受け取り、名前と年齢を表示するクラス
class Test:
    def __init__(self, name, age):
        self.name = name
        self.age = str(age)
        
    def __str__(self):
        print(f'{self.name}さんは{self.age}歳です。')
        
# RGBカラーコードを16進数表記に変換するクラス
class Rgb_to_Hex:
    def __init__(self, rgb):
        self.rgb = rgb
        
    def rgb_to_hex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.rgb[0], self.rgb[1], self.rgb[2])
    
class Extract_dominant_colors:
    def __init__(self, image, num_cluster):
        self.pixels = Image.open(image)
        self.num_cluster = num_cluster
    
    def execution(self):
        

# 画像からドミナントカラーを抽出する関数
def extract_dominant_colors(image, num_colors=10):
    image = Image.open(image)
    pixels = np.array(image).reshape(-1, 3)
    
    # k-meansクラスタリングを実行
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    
    # 各クラスタの中心点（ドミナントカラー）を取得
    dominant_colors = kmeans.cluster_centers_.astype(int)
    
    # 各ピクセルが属するクラスタのインデックスを取得
    labels = kmeans.labels_
    
    # 各ドミナントカラーの割合を計算
    color_counts = np.bincount(labels)
    total_pixels = len(labels)
    color_ratios = (color_counts / total_pixels) * 100
    color_ratios = color_ratios.round(2)
    
    # RGB値と割合のタプルのリストを返す
    return [(tuple(color), ratio) for color, ratio in zip(dominant_colors, color_ratios)]