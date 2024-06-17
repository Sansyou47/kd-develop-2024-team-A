# オリジナル画像の保存先
imgLocation_origin = 'images/origin/'
# リサイズ画像の保存先
imgLocation_resized = 'images/downsize/'
# アプリでサポートされている拡張子リスト
supportedExtentionList = ['jpg', 'jpeg', 'png']
# 暗号化された画像の保存先
imgLocation_encrypted = 'images/encrypted/'
# 復号化された画像の保存先
imgLocation_decrypted = 'images/decrypted/'

def xor_enc_dec(input, output, length, secret_key):
    count = 0
    for i in range(length):
        output[i] = input[i] ^ ord(secret_key[count])
        count += 1
        if count == len(secret_key):
            count = 0
        
def enc_file(inputfile, outputfile, secretKey):
    with open(inputfile, 'rb') as f:
        data = f.read()
    length = len(data)
    data = bytearray(data)
    xor_enc_dec(data, data, length, secretKey)
    with open(outputfile, 'wb') as f:
        f.write(data)
