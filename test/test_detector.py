import _init_path
import time

import cv2
from detector import Detector

detector = Detector()
image_path = 'D:\MyProject\Hololens2\online_project/test/image\hand5.jpg'
img = cv2.imread(image_path)
start = time.time()
res = detector.detect_from_image(img)
print(f'time: {time.time() - start}')
print(res)
cv2.imshow('image', detector.image_bgr)
detector.image_pil.show()
cv2.waitKey()
cv2.destroyAllWindows()