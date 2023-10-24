# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from UI.Animation.indexAnimation import IndexAnimation

class IndexAside(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUI()

    def setupUI(self):
        label_width = 200
        label_height = 60

        self.label0 = QtWidgets.QLabel(self.parent)
        self.label0.setText('Welcome')
        self.label0.setGeometry(0, 0, label_width, label_height)
        self.customLabelStyle(self.label0)

        self.label1 = QtWidgets.QLabel(self.parent)
        self.label1.setText('Read Objective Function')
        self.label1.setGeometry(0, label_height, label_width, label_height)
        self.customLabelStyle(self.label1)

        self.label2 = QtWidgets.QLabel(self.parent)
        self.label2.setText('Read Matrix')
        self.label2.setGeometry(0, label_height * 2, label_width, label_height)
        self.customLabelStyle(self.label2)

        self.label3 = QtWidgets.QLabel(self.parent)
        self.label3.setText('Calculate')
        self.label3.setGeometry(0, label_height * 3, label_width, label_height)
        self.customLabelStyle(self.label3)

        self.label_list = [self.label0, self.label1, self.label2, self.label3]

        self.remainder = QtWidgets.QLabel(self.parent)
        self.remainder.setStyleSheet("background:#006699")
        self.remainder.setGeometry(0, 240, 200, 400)

        self.indexAnimation = IndexAnimation(self.parent, self.label_list)
    
    def customLabelStyle(self, object):
        color = QColor(51, 153, 255, 255)
        object.setStyleSheet(f"background:{color.name()};color:white")
        object.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Normal))
        object.setAlignment(Qt.AlignmentFlag.AlignCenter)