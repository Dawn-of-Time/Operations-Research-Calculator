# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QPropertyAnimation, QPoint, QRect
class Utils:
    def __init__(self, object, parent) -> None:
        self.object = object
        self.parent = parent
    
    def shift(self, startValue, endValue, duration):
        moveAnimation = QPropertyAnimation(self.object, b"pos", self.parent)
        moveAnimation.setStartValue(startValue)
        moveAnimation.setEndValue(endValue)
        moveAnimation.setDuration(duration)
        return moveAnimation
    
    def scale(self, multiple:float, directionFlag:bool = True): # directionFlag: True:Fixed left; False:Fixed right
        xPosition = self.object.pos().x()
        yPosition = self.object.pos().y()
        width = self.object.width()
        height = self.object.height()
        scaleAnimation = QPropertyAnimation(self.object, b"geometry", self.parent)
        if directionFlag:
            scaleAnimation.setStartValue(QRect(xPosition, yPosition, width, height))
            scaleAnimation.setEndValue(QRect(xPosition, yPosition, width * multiple, height))
        else:
            scaleAnimation.setStartValue(QRect(xPosition, yPosition, width, height))
            scaleAnimation.setEndValue(QRect(xPosition - width * (multiple - 1), yPosition, width * multiple, height))
        scaleAnimation.setDuration(100)
        return scaleAnimation
    
    def scaleResume(self, resumeGeometry:list):
        scaleResumeAnimation = QPropertyAnimation(self.object, b"geometry", self.parent)
        scaleResumeAnimation.setStartValue(self.object.geometry())
        scaleResumeAnimation.setEndValue(resumeGeometry)
        scaleResumeAnimation.setDuration(100)
        return scaleResumeAnimation

    # TODO: Movedown or moveup could be a new way the dialog box pops up.
    def movedown(self):
        xPosition = self.object.pos().x()
        yPosition = self.object.pos().y()
        height = self.object.height()
        moveDownAnimation = QPropertyAnimation(self.object, b"pos", self.parent)
        moveDownAnimation.setStartValue(QPoint(xPosition, yPosition))
        moveDownAnimation.setEndValue(QPoint(xPosition, yPosition + height * 0.1))
        moveDownAnimation.setDuration(100)
        return moveDownAnimation
    
    def moveup(self):
        xPosition = self.object.pos().x()
        yPosition = self.object.pos().y()
        height = self.object.height()
        moveUpAnimation = QPropertyAnimation(self.object, b"pos", self.parent)
        moveUpAnimation.setStartValue(QPoint(xPosition, yPosition))
        moveUpAnimation.setEndValue(QPoint(xPosition, yPosition - height * 0.1))
        moveUpAnimation.setDuration(100)
        return moveUpAnimation
    

    # TODO: Add gradient animations in appropriate places to make the transition softer.
    def fadeAway(self):
        opacity = QtWidgets.QGraphicsOpacityEffect(self.parent)
        self.object.setGraphicsEffect(opacity)
        fadeAwayAnimation = QPropertyAnimation(opacity, b"opacity", self.parent)
        fadeAwayAnimation.setDuration(700)
        fadeAwayAnimation.setStartValue(1)
        fadeAwayAnimation.setEndValue(0)
        return fadeAwayAnimation
    
    def emerge(self):
        if (self.object.metaself.object().className() not in ['QButtonGroup', 'QVBoxLayout', 'QHBoxLayout', 'QGraphicsOpacityEffect']):
            opacity = QtWidgets.QGraphicsOpacityEffect(self.parent)
            self.object.setGraphicsEffect(opacity)
            emergeAnimation = QPropertyAnimation(opacity, b"opacity", self.parent)
            emergeAnimation.setDuration(700)
            emergeAnimation.setStartValue(0)
            emergeAnimation.setEndValue(1)
            return emergeAnimation
        return 0

    def colorGradient(self, startValue:str, endValue:str):
        colorGradientAnimation = QPropertyAnimation(self.object, b"styleSheet", self.parent)
        colorGradientAnimation.setDuration(700)
        colorGradientAnimation.setStartValue(startValue)
        colorGradientAnimation.setEndValue(endValue)
        return colorGradientAnimation
