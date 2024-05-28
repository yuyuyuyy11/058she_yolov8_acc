from flask import Flask, render_template, request, jsonify
from Yolov8Detector import Yolov8Detector
from BytetrackManager import BytetrackManager
import cv2
import os
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

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # 将文件保存到本地
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # 读取上传的视频文件
    video = cv2.VideoCapture(file_path)

    # 初始化结果列表
    all_results = []

    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # 进行目标检测
        results = detector.inferenc_image(frame)

        # 进行目标跟踪
        results_list = tracker.update(results)

        # 将检测结果添加到结果列表中
        all_results.append(results_list)

    video.release()

    # 返回所有检测结果
    return jsonify({'results': all_results})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=8080)
