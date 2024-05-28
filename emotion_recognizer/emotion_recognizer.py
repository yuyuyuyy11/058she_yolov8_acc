from keras.utils import img_to_array
import cv2
from keras.models import load_model
import numpy as np
from .utils import parameters as er_params
from PIL import Image, ImageDraw, ImageFont
import os

class EmotionRecognizer:
    def __init__(self) -> None:
        self.face_detector = cv2.CascadeClassifier(er_params['model']['face'])
        self.emotion_detector = load_model(er_params['model']['emotion'])

    def recognize_emotion_from_image(self, image_gray):  # 传入的人脸图片是灰度图
        faces = self.face_detector.detectMultiScale(
                                    image_gray, scaleFactor=1.1, minNeighbors=5, 
                                    minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) == 0:
            return None
        faces = sorted(faces, reverse=True, 
                    key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = image_gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = self.emotion_detector.predict(roi)[0]
        max_index = preds.argmax()
        prob = preds[max_index]
        return [[fX, fY, fX + fW, fY + fH], er_params['emotions'][max_index], prob]
    
    def recognize_emotion_from_path(self, image_path: str):
        image = cv2.imread(image_path)
        return self.recognize_emotion_from_image(image)
    
    def draw_on_image(self, image_pil, face_res):
        if face_res is not None:
            x1, y1, x2, y2 = face_res[0][0], face_res[0][1], face_res[0][2], face_res[0][3]
            draw = ImageDraw.Draw(image_pil)
            font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                'font/仿宋_GB2312.ttf'), 30)
            draw.text((x1, max(y1 - 30, 0)), f'{face_res[1]}:{face_res[2]:.3f}', font=font, fill='red')
            draw.rectangle([(x1, y1), (x2, y2)], outline='green', width=2)
    
