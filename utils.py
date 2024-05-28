import os

PROJ_DIR = os.path.dirname(__file__)
parameters = {
    'host': 'http://127.0.0.1',
    'image': {
        'before': os.path.join(PROJ_DIR, 'temp/before_image.jpg'),  # 处理前的图片路径
        'after': os.path.join(PROJ_DIR, 'temp/after_image.jpg')  # 处理后的图片路径
    },
    'ui': os.path.join(PROJ_DIR, 'ui/gui.ui'),
    'model': {
        'face': os.path.join(PROJ_DIR, 
                             'emotion_recognizer/models/haarcascade_frontalface_default.xml'),
        'emotion': os.path.join(PROJ_DIR, 
                                'emotion_recognizer/models/_mini_XCEPTION.102-0.66.hdf5')
    },
    'emotions': ["生气", 
                 "厌恶", 
                 "焦虑", 
                 "高兴", 
                 "悲伤", 
                 "惊讶", 
                 "中性"],
    'font': os.path.join(PROJ_DIR, 'font/仿宋_GB2312.ttf')
}