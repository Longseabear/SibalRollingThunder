# -*- coding: cp949 -*-

import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random
from PIL import ImageFont, ImageDraw, Image

h = 640
w = 480

class string_object(object):
    def __init__(self, string):
        self.str = string
        self.color = [random.randrange(0,256),random.randrange(0,256),random.randrange(0,256),0]
        self.size = 0
        self.position = [random.randrange(0,h),random.randrange(0,w)]
        self.alpha = 0

    def update(self):
        if self.size < 100:
            self.size += 1

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        self.strs = []
        self.image = np.zeros([480,640,3])
        self.dimensions = self.image.shape[1::-1]

        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)

        view = QGraphicsView(self)
        view.setScene(scene)


        layout = QVBoxLayout(self)
        layout.addWidget(view)

        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(80, 20)
        self.lineEdit.setFixedWidth(700)
        self.lineEdit.returnPressed.connect(self.onPress)
        layout.addWidget(self.lineEdit)

        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def onPress(self):
        self.strs.append(string_object(self.lineEdit.text()))
        print(self.lineEdit.text())
        self.lineEdit.setText("")

    def get_frame(self):
        frame = np.ones([480,640,3], np.uint8)
        img_pil = Image.fromarray(frame)
        for s in self.strs:
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype('./batang.ttc', s.size)
            draw.text((s.position[1],s.position[0]), s.str, font=font, fill=(s.color[0],s.color[1],s.color[2],255))
            s.update()
        frame = np.array(img_pil)
        self.strs[:] = [x for x in self.strs if x.size < 99]
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)


app = QApplication([])
win = MainWindow()
win.show()
app.exec()
