# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from UI.indexAside import IndexAside
from UI.Widget.buttonFrame import ButtonFrame

class WelcomeWidget(QtWidgets.QWidget): 
    def __init__(self): 
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.title = QtWidgets.QLabel('Operations Research', self)
        self.title.setFont(QFont('Microsoft YaHei UI', 42, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setGeometry(19, 50, 700, 100)

        self.subtitle = QtWidgets.QLabel('Calculator', self)
        self.subtitle.setFont(QFont('Microsoft YaHei UI', 36, QFont.Weight.Light))
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.subtitle.setGeometry(19, 160, 700, 60)

        self.startButtonFrame = ButtonFrame(self)
        self.startButtonFrame.getButton().clicked.connect(self.forward)

    def forward(self):
        stackedWidget:QtWidgets.QStackedWidget = self.parent()
        mainWidget:QtWidgets.QWidget = stackedWidget.parent()
        stackedWidget.setCurrentIndex(1)
        mainWidget.indexAside.indexAnimation.updateIndexAnimation(1, stackedWidget)