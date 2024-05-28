from .config import *
from .crnn import CRNNHandle
from .angnet import  AngleNetHandle
from .utils import draw_bbox, crop_rect, sorted_boxes, get_rotate_crop_image
from .dbnet.dbnet_infer import DBNET
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import copy
import traceback

class  OcrHandle(object):
    def __init__(self):
        self.text_handle = DBNET(model_path)
        self.crnn_handle = CRNNHandle(crnn_model_path)
        if angle_detect:
            self.angle_handle = AngleNetHandle(angle_net_path)


    def crnnRecWithBox(self,im, boxes_list,score_list):
        """
        crnn模型，ocr识别
        @@model,
        @@converter,
        @@im:Array
        @@text_recs:text box
        @@ifIm:是否输出box对应的img

        """
        results = []
        boxes_list = sorted_boxes(np.array(boxes_list))

        line_imgs = []
        for index, (box, score) in enumerate(zip(boxes_list[:angle_detect_num], score_list[:angle_detect_num])):
            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))
            partImg = Image.fromarray(partImg_array).convert("RGB")
            line_imgs.append(partImg)

        angle_res = False
        if angle_detect:
            angle_res = self.angle_handle.predict_rbgs(line_imgs)

        count = 1
        for index, (box ,score) in enumerate(zip(boxes_list,score_list)):

            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))


            partImg = Image.fromarray(partImg_array).convert("RGB")

            if angle_detect and angle_res:
                partImg = partImg.rotate(180)


            if not is_rgb:
                partImg = partImg.convert('L')

            try:
                if is_rgb:
                    simPred = self.crnn_handle.predict_rbg(partImg)  ##识别的文本
                else:
                    simPred = self.crnn_handle.predict(partImg)  ##识别的文本
            except Exception as e:
                print(traceback.format_exc())
                continue

            if simPred.strip() != '':
                # results.append([tmp_box,"{}、 ".format(count)+  simPred,score])
                results.append([tmp_box, simPred, score])
                count += 1

        return results


    def text_predict_from_image(self, image_bgr, short_size=320):
        boxes_list, score_list = self.text_handle.process(np.asarray(image_bgr, dtype=np.uint8), short_size=short_size)
        result = self.crnnRecWithBox(np.array(image_bgr), boxes_list, score_list)
        return result

    def text_predict_from_image_path(self, image_path, short_size=320):
        img = cv2.imread(image_path)
        return self.text_predict_from_image(img, short_size=short_size)
    
    def draw_on_image(self, image_pil, ocr_res, shift_x=0):
        if ocr_res is not None:
            draw = ImageDraw.Draw(image_pil)
            font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                'font/仿宋_GB2312.ttf'), 20)
            for line in ocr_res:
                x1, y1 = line[0][0][0], line[0][0][1]
                draw.text((x1 + shift_x, max(y1 - 20, 0)), f'{line[1]}', font=font, fill='red')
                poly = [(i[0] + shift_x, i[1]) for i in line[0].tolist()]
                draw.polygon(poly, outline='green', width=2)

if __name__ == "__main__":
    import cv2
    image_path = '../test/ocr1.png'
    img = cv2.imread(image_path)

    ocrHandle = OcrHandle()
    result = ocrHandle.text_predict_from_image(img, short_size=320)
    
    print(result)
    image_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ocrHandle.draw_on_image(image_pil, result)
    image_pil.show()
