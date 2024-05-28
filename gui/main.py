import os
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import sys
import time
from PIL import Image
import threading
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

INFO_COLOR = 'black'
SUC_COLOR = 'green'
ERR_COLOR = 'red'
WOR_COLOR = '#DCDCA1'
IMG_WIDTH = 360
IMG_HEIGHT = 270
TMP_IMG_PATH = os.path.join(BASE_DIR, 'temp/tmp_image.jpg')
REFRESH_TIME_SLOT = 50

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__set_ui()
        self.__init_params()
        self.__init_widgets()
        self.__bind_all_functions()
        
    def __set_ui(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'gui.ui')
        loadUi(ui_path, self)

    def __init_params(self):
        pass

    def output_log(self, msg, type='info'):
        """type -> ['info', 'suc', 'err', 'wor']

        """
        if type == 'suc':
            s = f"<span style='color:{SUC_COLOR};'>{msg}</span>"
        elif type == 'err':
            s = f"<span style='color:{ERR_COLOR};'>{msg}</span>"
        elif type == 'wor':
            s = f"<span style='color:{WOR_COLOR};'>{msg}</span>"
        else:
            s = f"<span style='color:{INFO_COLOR};'>{msg}</span>"
        self.logOutput.append(s)
        self.logOutput.repaint()

    def __init_widgets(self):
        self.portInput.setValidator(QIntValidator())  # 设置仅能输入整数
        self.scene = QGraphicsScene()
        self.imageView.setFixedSize(IMG_WIDTH, IMG_HEIGHT)
        self.imageView.setScene(self.scene)
        self.show_image_from_path()

    def __bind_all_functions(self):
        self.runBtn.clicked.connect(self.start_flask_app)
    
    def start_flask_app(self):
        if self.portInput.text() != '' and 0<= int(self.portInput.text()) <= 65535:
            port = int(self.portInput.text())
            self.output_log(f'正在端口号{port}启动Flask APP...')

            def run_script():
                os.system(f"python {os.path.join(BASE_DIR, 'app/app.py')} --port {port}")
            self.app_t = threading.Thread(target=run_script)
            self.app_t.start()
            time.sleep(5)
            
            self.output_log('Flask APP启动成功!', 'suc')
        else:
            self.output_log('端口号必须设置0~65535', 'err')

    def openFileDialog(self):
        # 点击按钮，选择文件
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self,
                                              "选择文件",
                                              os.getcwd(),
                                              "CSV Files (*.csv);;All Files (*)",
                                              options=options)
        if path:
            print(f"selected file: {path}")
            self.file_path = path
            self.df_data = pd.read_csv(self.file_path)

    def show_image_from_path(self, 
                             image_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp/tmp_image.jpg')):
        self.scene.clear()
        image_pil = Image.open(image_path)
        w, h = image_pil.size
        
        # 计算宽高比
        aspect_ratio = w / h
        
        # 根据宽高比确定缩放后的图片尺寸
        if IMG_WIDTH / IMG_HEIGHT > aspect_ratio:
            # 以高度为准
            scaled_width = int(IMG_HEIGHT * aspect_ratio)
            scaled_height = IMG_HEIGHT
        else:
            # 以宽度为准
            scaled_width = IMG_WIDTH
            scaled_height = int(IMG_WIDTH / aspect_ratio)
        
        # 缩放图片
        image_pil = image_pil.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        
        # 创建白色背景 QPixmap
        background_pixmap = QPixmap(QSize(IMG_WIDTH, IMG_HEIGHT))
        background_pixmap.fill(Qt.white)  # 用白色填充
        # 将缩放后的图片绘制到背景 QPixmap 上
        painter = QPainter(background_pixmap)
        painter.drawPixmap((IMG_WIDTH - scaled_width) // 2, (IMG_HEIGHT - scaled_height) // 2, scaled_width, scaled_height, QPixmap.fromImage(image_pil.toqimage()))
        painter.end()
        
        # 创建 QGraphicsPixmapItem 并添加到场景中
        pixmap_item = QGraphicsPixmapItem(background_pixmap)
        self.scene.addItem(pixmap_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
