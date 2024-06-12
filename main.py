import os
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import sys
import time
import requests
from PIL import Image
import threading
from utils import parameters

INFO_COLOR = 'black'
SUC_COLOR = 'green'
ERR_COLOR = 'red'
WOR_COLOR = '#DCDCA1'
IMG_WIDTH = 360
IMG_HEIGHT = 270
UPDATE_TIME_INTERVAL = 50

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__set_ui()
        self.__init_params()
        self.__init_widgets()
        self.__bind_all_functions()
        self.check_flask_app_is_running()
        
    def __set_ui(self):
        ui_path = parameters['ui']
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
        self.switch_status(False)
        self.update_image()

    def __bind_all_functions(self):
        self.runBtn.clicked.connect(self.start_flask_app)
    
    def init_timer(self):
         # Set up a timer to update the image periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(UPDATE_TIME_INTERVAL)  # interval in milliseconds

    def update_image(self):
        try:
            self.show_image_from_path()
        except:
            pass


    def switch_status(self, is_runing):
        self.closeBtn.setVisible(is_runing)
        self.runBtn.setVisible(not is_runing)

    def check_flask_app_is_running(self):
        if self.portInput.text() != '' and 0<= int(self.portInput.text()) <= 65535:
            port = int(self.portInput.text())
            try:
                requests.get(f"{parameters['host']}:{port}")
                self.switch_status(True)
                self.init_timer()
                self.output_log(f'Flask APP已经在启动在端口{port}')
                self.switch_status(True)
            except:
                pass

    def start_flask_app(self):
        if self.portInput.text() != '' and 0<= int(self.portInput.text()) <= 65535:
            port = int(self.portInput.text())
            self.output_log(f'正在端口号{port}启动Flask APP...')

            def run_script():
                os.system(f"python {os.path.join(os.path.dirname(__file__), 'app/app.py')} --port {port}")
            self.app_t = threading.Thread(target=run_script)
            self.app_t.start()

            while 1:
                try:
                    requests.get(f"{parameters['host']}:{port}")
                    self.switch_status(True)
                    self.init_timer()
                    break
                except:
                    pass
            
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
                             image_path=parameters['image']['after']):
        # 创建白色背景 QPixmap
        scaled_ratio = 0.9
        background_pixmap = QPixmap(QSize(int(IMG_WIDTH * scaled_ratio), int(IMG_HEIGHT * scaled_ratio)))
        background_pixmap.fill(Qt.white)  # 用白色填充

        if not os.path.exists(image_path):
            image_pil = None
        else:
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
            
            # 将缩放后的图片绘制到背景 QPixmap 上
            painter = QPainter(background_pixmap)
            painter.drawPixmap((IMG_WIDTH - scaled_width) // 2, (IMG_HEIGHT - scaled_height) // 2, scaled_width, scaled_height, QPixmap.fromImage(image_pil.toqimage()))
            painter.end()
        # 创建 QGraphicsPixmapItem 并添加到场景中
        pixmap_item = QGraphicsPixmapItem(background_pixmap)
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.scene.addItem(pixmap_item)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '关闭窗口', '您确定要关闭窗口吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # 接受关闭事件
        else:
            event.ignore()  # 忽略关闭事件，窗口不会关闭

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
