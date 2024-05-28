import base64
import io
import json
import os
import sys
import numpy as np
from PIL import Image, ImageOps



def save_file_str_to(f_str: str, to_path: str, flip=False):
    dirname = os.path.dirname(to_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    image = Image.open(io.BytesIO(base64.b64decode(f_str)))
    if flip:
        image = Image.fromarray(np.flipud(np.array(image))) # 将图片转换为灰度格式并上下翻转
    image.save(to_path, format='JPEG')
    