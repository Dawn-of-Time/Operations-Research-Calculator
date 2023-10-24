# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QRect
class TopBar(QtWidgets.QFrame):
    def __init__(self, parent:QtWidgets.QWidget):
        super(TopBar, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(0, 0, 738, 50)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background-color: #00cccc')
        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.buttonStyleSheet = 'QPushButton {background-color: #00cccc;border: none} QPushButton:hover {background-color: #00ccff} QPushButton:pressed {background-color: #00bbff}'

        self.backButton = QtWidgets.QPushButton(self)
        self.backButton.setMinimumHeight(50)
        self.backButton.setStyleSheet(self.buttonStyleSheet)
        self.backButton.setIcon(QIcon('res/icon/back.png'))

        self.continueButton = QtWidgets.QPushButton(self)
        self.continueButton.setMinimumHeight(50)
        self.continueButton.setStyleSheet(self.buttonStyleSheet)
        self.continueButton.setIcon(QIcon('res/icon/continue.png'))

        self.infoButton = QtWidgets.QPushButton(self)
        self.infoButton.setMinimumHeight(50)
        self.infoButton.setStyleSheet(self.buttonStyleSheet)
        self.infoButton.setIcon(QIcon('res/icon/success.png'))
        self.infoButton.setIconSize(QSize(20, 20))

        self.buttonLayout.addWidget(self.backButton, 1)
        self.buttonLayout.addWidget(self.infoButton, 8)
        self.buttonLayout.addWidget(self.continueButton, 1)
        self.buttonLayout.setGeometry(QRect(222, 0, 738, 50))
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.buttonLayout)

        self.backButton.clicked.connect(self.backward)
        self.continueButton.clicked.connect(self.forward)

    def infoButtonResume(self):
        self.infoButton.setText(None)
        self.infoButton.setStyleSheet(self.buttonStyleSheet)
        self.infoButton.setIcon(QIcon('res/icon/success.png'))
        self.infoButton.setIconSize(QSize(20, 20))

    def backward(self):
        index = self.parent().parent().currentIndex() - 1
        self.parent().parent().setCurrentIndex(index)
        self.parent().parent().parent().indexAside.indexAnimation.updateIndexAnimation(index, self.parent())

    def forward(self):
        index = self.parent().parent().currentIndex()
        errorNum = self.parent().verifyAll()
        if errorNum == 0:
            index = self.parent().parent().currentIndex() + 1
            self.parent().parent().setCurrentIndex(index)
            self.parent().parent().parent().indexAside.indexAnimation.updateIndexAnimation(index, self.parent())

        
