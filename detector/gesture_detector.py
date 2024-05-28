import sys
import os

import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .hand_detector import HandDetector
from emotion_recognizer import EmotionRecognizer
from chineseocr_lite import OcrHandle
import cv2
from PIL import Image

class GestureDetector:
    def __init__(self):
        self.emotion_recognizer = EmotionRecognizer()
        self.hand_detector = HandDetector()
        self.ocr_handle = OcrHandle()
        self.shift_x = 0
    
    def detect_one_image(self, image_bgr):
        """检测一帧图片
        
        Return: [face_res, ocr_res]
        """
        image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        face_res = ocr_res = None
        face_res = self.emotion_recognizer.recognize_emotion_from_image(image_gray)
        # print(f'face: {face_res}')
        # 人脸的优先级高于手势
        if face_res is None:  # 当不存在人脸时，进行手部关键点检测
            pos = self.hand_detector.detect_thumb_tips(image_bgr)
            # print(f'pos: {pos}')
            if len(pos) == 2:
                self.shift_x = pos[0][0]
                cropped_image = self.hand_detector.crop_image_from_tips_pos(image_bgr, pos)
                ocr_res = self.ocr_handle.text_predict_from_image(cropped_image, 640)
        return [face_res, ocr_res]

    def draw_on_image(self, image_pil, face_res, ocr_res):
        self.hand_detector.draw_on_image(image_pil)
        self.emotion_recognizer.draw_on_image(image_pil, face_res)
        self.ocr_handle.draw_on_image(image_pil, ocr_res, self.shift_x)

if __name__ == '__main__':
    gesture_detector = GestureDetector()
    res, img = gesture_detector.detect_one_image_from_path('D:\MyProject\Hololens2\online_project\\test/face1.jpg')
    print(res)
    cv2.imshow('image', img)
    Image.fromarray()
    cv2.imshow('image_drawn', gesture_detector.draw_on_image(img, res[0]))
    cv2.waitKey()
    cv2.destroyAllWindows()
