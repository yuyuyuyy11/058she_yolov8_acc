import time
import cv2
import _init_path
from yolo.Yolov8Detector import Yolov8Detector

detector = Yolov8Detector()
img = cv2.imread('image/hand1.jpg')
t1 = time.time()
res = detector.inferenc_image(img)
t2 = time.time()
print(res)
print(f"time: {t2 - t1}")
