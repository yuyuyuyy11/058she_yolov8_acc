from flask import Flask, render_template, request, jsonify
from Yolov8Detector import Yolov8Detector
from BytetrackManager import BytetrackManager
import cv2
import os
from collections import OrderedDict
app = Flask(__name__)
detector = Yolov8Detector()
tracker = BytetrackManager()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/detect_and_track', methods=['POST'])
def detect_and_track():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('file')  # 获取上传的所有文件

    all_results = []  # 初始化结果列表

    for file in files:
        if file.filename == '':
            continue
        
        # 将文件保存到本地
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 读取上传的图片文件
        frame = cv2.imread(file_path)

        # 进行目标检测
        results = detector.inferenc_image(frame)

        # 进行目标跟踪
        results_list = tracker.update(results)

       #转换为字典格式
        detections = []
        for result in results_list:
            detection=OrderedDict({
                "position":[result[2],result[3],result[4],result[5]],
                "confidence":result[1],
                "label":result[0]
            })
            detections.append(detection)
        all_results.append(detections)
    return jsonify({'results':all_results})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=8080)
