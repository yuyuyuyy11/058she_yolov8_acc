from .ultralytics import YOLO
import cv2
from .ultralytics.utils.plotting import Annotator
from .utils import *

class Yolov8Detector(object):
    def __init__(self, weights=parameters['weight']):
        self.model = YOLO(weights)  # load a pretrained model (recommended for training)

    def inferenc_image(self, opencv_image):
        results = self.model.predict(opencv_image, verbose=False, conf=0.2, device='cuda:0')  # predict on an image
        return results

    def draw_image(self, result_list, image_pil):
        ann = Annotator(image_pil, pil=True)  # 传入image_pil
        for result in result_list:
            label = result[0] + "," + str(result[1]) + "," + str(result[6])
            ann.box_label(result[2:6], label)




if __name__ == '__main__':
    detector = Yolov8Detector()
    img = cv2.imread('images/bus.jpg')
    detector.inferenc_image(img)
