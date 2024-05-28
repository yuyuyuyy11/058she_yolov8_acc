import cv2
from Yolov8Detector import *
from BytetrackManager import *
detector = Yolov8Detector()
tracker = BytetrackManager()
# 定义一个函数，用于读取帧图像
def read_frame(file_path):
    frame = cv2.imread(file_path)  # 从文件路径读取帧图像
    return frame
frame_file = "./images/bus.jpg"  # 单独的帧图像文件路径
# 读取单独的帧图像
frame = read_frame(frame_file)
# 对单独的帧图像进行目标检测
results = detector.inferenc_image(frame)
# 更新目标跟踪
results_list = tracker.update(results)
# 在帧上绘制边界框
annotated_frame = detector.draw_image(results_list, frame)
# 显示帧
cv2.imshow('frame', annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
