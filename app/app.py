import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJ_DIR)
from detector import Detector
                
from flask import Flask, render_template, request
import argparse
from utils import *
import json


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
    
    output_path = os.path.join(PROJ_DIR, 'temp/tmp_image.jpg')
    save_file_str_to(file_str, output_path, False)
    print(f'save file to: {output_path}')
    res = detector.detect_from_path(output_path)
    print(res)
    return json.dumps(res)

def main():
    parser = argparse.ArgumentParser(description="启动后端Flask应用")
    parser.add_argument('-p', '--port', type=str, required=True, help='Flask APP运行的端口号')
    args = parser.parse_args()
    app.run('0.0.0.0', port=args.port, debug=True)

if __name__ == '__main__':
    main()