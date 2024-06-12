import sys
import os

import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .gesture_detector import GestureDetector
from yolo import YoloPredictor
import cv2
from PIL import Image

class Detector:
    def __init__(self):
        self.gesture_detector = GestureDetector()
        self.yolo_predictor = YoloPredictor()
        self.image_bgr = None  # image to compute
        self.image_pil = None  # image to show
    
    def detect_from_image(self, image_bgr):
        self.image_bgr = image_bgr
        self.image_pil = Image.fromarray(cv2.cvtColor(self.image_bgr, cv2.COLOR_BGR2RGB))
        # Yolo
        yolo_res = self.yolo_predictor.detect_object_from_image(self.image_bgr)
        print(f'yolo: {yolo_res}')
        self.yolo_predictor.draw_on_image(self.image_pil, yolo_res)
        # OCR and emotion
        face_res, ocr_res = self.gesture_detector.detect_one_image(self.image_bgr)
        self.gesture_detector.draw_on_image(self.image_pil, face_res, ocr_res)
        dict_res = self.cvt_res_to_dict(yolo_res, face_res, ocr_res)
        return dict_res

    def detect_from_path(self, image_path):
        return self.detect_from_image(cv2.imread(image_path))
    
    def cvt_res_to_dict(self, yolo_res, face_res, ocr_res):
        res = {
            'yolo': {
                'objects': []
                }, 
            'face': {}, 
            'ocr': {}
        }
        if yolo_res:
            for item in yolo_res:
                res['yolo']['objects'].append({
                    'id': item[6],
                    'label': item[0],
                    'confidence': item[1],
                    'positions': item[2:6]
                })
        if face_res:
            res['face'] = {
                'exists': True,
                'emotion': {
                    'label': face_res[1],
                    'confidence': float(face_res[2])
                }
            }
            res['ocr'] = {
                'exists': False,
                'lines': []
            }
        else:
            res['face'] = {
                'exists': False,
                'emotion': {}
            }
            if ocr_res:
                lines = []
                for line in ocr_res:
                    lines.append({
                        'line': line[1],
                        'position': line[0].astype('float').tolist(),
                        'confidence': float(line[2])
                    })
                res['ocr'] = {
                    'exists': True,
                    'lines': lines
                }
            else:
                res['ocr'] = {
                    'exists': False,
                    'lines': []
                }
        return res
