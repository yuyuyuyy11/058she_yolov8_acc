import base64
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJ_DIR)
import numpy as np
from utils import *
from detector import Detector
from flask import Flask, render_template, request
import argparse
import json
from PIL import Image
import io


detector = Detector()
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello~'

@app.route('/upload', methods=['POST'])
def upload():
    file_str = request.json.get('file')
    if file_str is None:
        return 'error'
    
    output_path = parameters['image']['before']
    save_file_str_to(file_str, output_path, False)
    print(f'save file to: {output_path}')
    res = detector.detect_from_path(output_path)
    print(f'result: {res}')
    detector.image_pil.save(parameters['image']['after'])
    return json.dumps(res)


def save_file_str_to(f_str: str, to_path: str, flip=False):
    dirname = os.path.dirname(to_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    image = Image.open(io.BytesIO(base64.b64decode(f_str)))
    if flip:
        image = Image.fromarray(np.flipud(np.array(image))) # 将图片转换为灰度格式并上下翻转
    image.save(to_path, format='JPEG')
    
def main():
    parser = argparse.ArgumentParser(description="启动后端Flask应用")
    parser.add_argument('-p', '--port', type=str, required=True, help='Flask APP运行的端口号')
    args = parser.parse_args()
    app.run('0.0.0.0', port=args.port, debug=True)

if __name__ == '__main__':
    main()