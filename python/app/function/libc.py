from flask import Blueprint
from function import variable
import ctypes

# コンパイル済みのC言語のライブラリを読み込む
libc = ctypes.CDLL(variable.libLocation + 'bit-convert.so')

app = Blueprint("libc", __name__)

@app.route('/function/conv_bit')
def conv_bit():
    input_file = '/app/function/images/input.jpg'
    output_file = '/app/function/images/output.jpg'
    bitdepth = 4
    
    # C言語の関数を呼び出す
    libc.convert_bit_depth(input_file, output_file)
    return "Hello, conv_bit!"