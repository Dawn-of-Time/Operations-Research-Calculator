# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QParallelAnimationGroup, QPoint
from UI.Animation.utils import Utils
class IndexAnimation:
    def __init__(self, parent:QtWidgets.QWidget, label_list:list) -> None:
        self.parent = parent
        self.indexAnimation = None
        self.labelList = label_list
        self.initIndexAnimation()
    
    def initIndexAnimation(self):
        self.aniBackground = QtWidgets.QLabel(self.parent)
        self.aniBackground.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0.8 #0099cc, stop:1 #ffffff);")
        self.background = QtWidgets.QLabel(self.parent)
        self.background.setStyleSheet("background:#0099cc")
        # Mark the original position to restore the position later.
        self.sacleResumeList = [label.geometry() for label in self.labelList]
    
    def updateIndexAnimation(self, index:int, parent):
        if self.indexAnimation != None:
            self.indexAnimation.stop()
        self.aniBackground.setGeometry(0, 60 * index, 300, 60)
        self.background.setGeometry(0, 60 * index, 222, 60)
        # Animation 1: Change of color.
        for i in range(len(self.labelList)):
            if i == index:
                self.labelList[i].setStyleSheet("background:transparent;color:white")
            elif i == index + 1:
                self.labelList[i].setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, "
            "stop:0.8 #006699, stop:1 #3b3b3b);color:white")
            else:
                self.labelList[i].setStyleSheet("background:#006699;color:white")
        # Animation 2: Scale Animation.
        group = QParallelAnimationGroup(self.parent)
        for i in range(len(self.labelList)):
            if i == index:
                scaleAnimation0 = Utils(self.labelList[i], parent).scale(1.1)
                group.addAnimation(scaleAnimation0)
                scaleAnimation1 = Utils(self.background, parent).scale(1.1)
                group.addAnimation(scaleAnimation1)
                scaleAnimation2 = Utils(self.aniBackground, parent).scale(1.1)
                group.addAnimation(scaleAnimation2)
            else:
                scaleResumeAnimation = Utils(self.labelList[i], parent).scaleResume(self.sacleResumeList[i])
                group.addAnimation(scaleResumeAnimation)
        # Animation 3: Shift Animation.
        self.labelList[index].stackUnder(self.parent.stackedWidget)
        self.aniBackground.stackUnder(self.labelList[index])
        self.background.stackUnder(self.aniBackground)
        self.parent.devide.stackUnder(self.background)
        self.indexAnimation = Utils(self.aniBackground, parent).shift(QPoint(-400, self.aniBackground.y()), QPoint(self.aniBackground.x(), self.aniBackground.y()), 3000)
        self.indexAnimation.setLoopCount(-1)

        group.addAnimation(self.indexAnimation)
        group.start()