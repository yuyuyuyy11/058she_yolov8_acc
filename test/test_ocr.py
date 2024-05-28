import _init_path
from chineseocr_lite.model import OcrHandle
import cv2
from PIL import Image


image_path = 'ocr1.png'
img = cv2.imread(image_path)

ocrHandle = OcrHandle()
result = ocrHandle.text_predict_from_image(img, short_size=320)

print(result)
image_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ocrHandle.draw_on_image(image_pil, result)
image_pil.show()
while 1:
    print(1)