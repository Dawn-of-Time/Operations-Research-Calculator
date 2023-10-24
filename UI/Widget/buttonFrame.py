# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QTimer, Qt, QRectF, QSize, QEvent
from PyQt6.QtGui import QCursor, QPainter, QBrush, QColor, QPainterPath, QIcon, QFont, QRegion
class ButtonFrame(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(ButtonFrame, self).__init__(parent)
        self.startButton = QtWidgets.QPushButton(self)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(320, 300, 100, 100)
        self.setStyleSheet("border-radius: 50px; background-color: #0099ff;")
        self.startButton.setFixedSize(100, 100)
        self.startButton.setFont(QFont('Microsoft YaHei UI', 16, QFont.Weight.Light))
        self.startButton.setStyleSheet("QPushButton {border-radius: 50px; background-color: transparent} QPushButton:pressed {background-color: #00ccff}")
        self.startButton.setIcon(QIcon('res/icon/continue.png'))
        self.startButton.setIconSize(QSize(40, 40))
        self.setMask(QRegion(-2,-2,104,104,QRegion.RegionType.Ellipse))

    def animation(self):
        self.hoverFlag = True
        self.center = None
        self.radius = 10
        self.maxRadius = (self.width() ** 2 + self.height() ** 2) ** 0.5
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.scale)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hoverFlag = True
        self.radius = 10
        self.center = event.position()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.scale)
        self.timer.start()

    def leaveEvent(self, event):
        self.hoverFlag = False
        self.radius = self.maxRadius
        self.center = self.mapFromGlobal(QCursor.pos())
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.scale)
        self.timer.start()

    def scale(self):
        if self.hoverFlag:
            self.radius += 5
            if self.radius > self.maxRadius:
                self.timer.stop()
                return
        else:
            self.radius -= 5
            if self.radius < 0:
                self.timer.stop()
                return
        self.update()
      
    def paintEvent(self, event):
        super(ButtonFrame, self).paintEvent(event)
        if self.center == None or self.hoverFlag == False and self.radius < 2:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        brush = QBrush(QColor(0, 204, 255))
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.width()/2, self.width()/2)
        painter.setClipPath(path)

        painter.drawEllipse(self.center, self.radius, self.radius)

    def showEvent(self, event):
        super().showEvent(event)
        self.animation()

    def getButton(self):
        return self.startButton
