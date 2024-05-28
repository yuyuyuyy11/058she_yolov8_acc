import cv2
from .Yolov8Detector import *
from .BytetrackManager import *
import time


class YoloPredictor:
    def __init__(self):
        self.detector = Yolov8Detector()
        self.tracker = BytetrackManager()

    def detect_object_from_image(self, image):
        results = self.detector.inferenc_image(image)
        results_list = self.tracker.update(results)
        return results_list

    def detect_object_from_path(self, image_path):
        image = cv2.imread(image_path)
        return self.detect_object_from_image(image)

    def draw_on_image(self, image_pil, results):
        if results is not None:
            self.detector.draw_image(results, image_pil)
    

if __name__ == '__main__':
    video_file = "./images/test.mp4"
    cap = cv2.VideoCapture(video_file)
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("video fps={}, width={}, height={}".format(frame_fps, frame_width, frame_height))
    yoloPredictor = YoloPredictor()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        start = time.time()
        res = yoloPredictor.detect_object_from_image(frame)
        t = time.time() - start
        fps = 1.0 / t
        frame = yoloPredictor.draw_on_image(frame, res)
        frame = cv2.putText(frame, f'FPS: {t:.2f}', (10, 20), 1, 1, (0, 0, 255), 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
