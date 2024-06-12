import base64
import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJ_DIR)
from chineseocr_lite.model import OcrHandle
from emotion_recognizer.emotion_recognizer import EmotionRecognizer
import numpy as np
from utils import *
from detector import Detector
from flask import Flask, request
import argparse
import json
from PIL import Image
import io

detector = Detector()
ocr_handle = detector.gesture_detector.ocr_handle
emotion_recognizer = detector.gesture_detector.emotion_recognizer
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
    res = detector.detect_from_path(output_path)
    print(f'result: {res}')
    detector.image_pil.save(parameters['image']['after'])
    return json.dumps(res)

@app.route('/<api>', methods=['POST'])  # /face_emotion_recognition, /ocr
def run_api(api):
    file_str = request.json.get('file')
    if file_str is None:
        return 'error'
        
    output_path = parameters['image']['before']
    save_file_str_to(file_str, output_path, False)
    # 将保存到本地的文件的路径发送给识别程序
    if api == 'ocr':
        result = ocr_handle.text_predict_from_image_path(output_path)
        result = cvt_ocr_result_to_json(result)
    elif api == 'face_emotion_recognition':
        result = emotion_recognizer.recognize_emotion_from_path(output_path)
        print(f'result: {result}')
        result = cvt_fer_result_to_json(result)
    else:
        return 'invalid api'
    print(f'result: {result}')
    return result

def save_file_str_to(f_str: str, to_path: str, flip=False):
    dirname = os.path.dirname(to_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    image = Image.open(io.BytesIO(base64.b64decode(f_str)))
    if flip:
        image = Image.fromarray(np.flipud(np.array(image))) # 将图片转换为灰度格式并上下翻转
    image.save(to_path, format='JPEG')
    print(f'save file to: {to_path}')

    
def cvt_ocr_result_to_json(result, to_str=False):
    data_obj = {
        "data": {
            "lines": []
        }
    }
    if result:
        for line in result:
            line_obj = {
                "text": line[1],
                "confidence": float(line[2]),
                "position": [[float(line[0]), float(line[1])] for line in line[0]]  # [x1, y1, x2, y2]
            }
            data_obj["data"]["lines"].append(line_obj)
    if to_str: data_obj = json.dumps(data_obj)
    return data_obj

def cvt_fer_result_to_json(result, to_str=False):
    data_obj = { "data": {} }
    if result:
        data_obj["data"] = {
            "emotion": result[1],
            "confidence": float(result[2])
        }
    if to_str: data_obj = json.dumps(data_obj)
    return data_obj

def main():
    parser = argparse.ArgumentParser(description="启动后端Flask应用")
    parser.add_argument('-p', '--port', type=str, default=5000, help='Flask APP运行的端口号')
    args = parser.parse_args()
    app.run('0.0.0.0', port=args.port, debug=True)

if __name__ == '__main__':
    main()