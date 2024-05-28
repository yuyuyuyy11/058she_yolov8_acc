import cv2
from Yolov8Detector import *
from BytetrackManager import *
detector = Yolov8Detector()
tracker = BytetrackManager()
video_file = "./images/test.mp4"
cap = cv2.VideoCapture(video_file)
frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("video fps={}, width={}, height={}".format(frame_fps, frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = detector.inferenc_image(frame)
    results_list = tracker.update(results)
    frame = detector.draw_image(results_list, frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
