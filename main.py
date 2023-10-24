# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  


import sys
import ctypes
from UI.welcomeWidget import WelcomeWidget
from UI.chooseWidget import ChooseWidget
from UI.matrixWidget import MatrixWidget
from UI.calculateWidget import CalculateWidget
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QIcon
from UI.indexAside import IndexAside

class MainWidget(QtWidgets.QWidget): 
    def __init__(self): 
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Operations Research Calculator')
        self.setWindowIcon(QIcon('res/icon/main.ico'))
        self.setFixedSize(960, 640)
        self.setStyleSheet("background:white")
        # Modify the taskbar icon.
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        
        self.devide = QtWidgets.QLabel(self)
        self.devide.setGeometry(200, 0, 22, 640)
        self.devide.setStyleSheet("background:#4682b4")

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(222, 0, 738, 640)

        self.indexAside = IndexAside(self)

        self.welcomeWidget = WelcomeWidget()
        self.chooseWidget = ChooseWidget()
        self.matrixWidget = MatrixWidget(self.chooseWidget)
        self.calculateWidget = CalculateWidget(self.chooseWidget,self.matrixWidget)
        self.stackedWidget.addWidget(self.welcomeWidget)
        self.stackedWidget.addWidget(self.chooseWidget)
        self.stackedWidget.addWidget(self.matrixWidget)
        self.stackedWidget.addWidget(self.calculateWidget)
        self.stackedWidget.setCurrentIndex(0)
        self.indexAside.indexAnimation.updateIndexAnimation(0, self)

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()
    sys.exit(application.exec())