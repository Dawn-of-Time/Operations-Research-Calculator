# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import re
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt
from UI.topBar import TopBar
from Utils.utilsErrorHandle import ChooseErrorHandle

class ChooseWidget(QtWidgets.QWidget):
    infoToMatrix = pyqtSignal(list)
    def __init__(self): 
        super().__init__()
        self.errorDict:dict = {1: False, 2: False, 3:False}
        self.setupUI()
    
    def setupUI(self):
        self.topBar = TopBar(self)

        self.sectionStyleSheet = 'background-color: white; border-bottom: 5px solid #006699'
        self.typeStyleSheet = "background-color: white; padding: 0px 30px; border-left: 10px solid #006699;\
        border-top: 1px solid #006699; border-bottom: 1px solid #006699; border-right: 1px solid #006699;"

        self.typeSection = QtWidgets.QLabel('1.Type of Objective Function', self)
        self.typeSection.setGeometry(50, 100, 550, 60)
        self.typeSection.setFont(QFont('Microsoft YaHei UI', 22, QFont.Weight.Bold))
        self.typeSection.setStyleSheet(self.sectionStyleSheet)

        self.maxType = QtWidgets.QRadioButton("max", self)
        self.maxType.setFont(QFont('Times New Roman', 18, QFont.Weight.Normal, True))
        self.maxType.setGeometry(50, 200, 600, 50)
        self.maxType.setStyleSheet(self.typeStyleSheet)
        self.maxType.toggled.connect(self.choiceHandle)
        self.maxType.toggled.connect(self.verifyType)

        self.minType = QtWidgets.QRadioButton("min", self)
        self.minType.setFont(QFont('Times New Roman', 18, QFont.Weight.Normal, True))
        self.minType.setGeometry(50, 270, 600, 50)
        self.minType.setStyleSheet(self.typeStyleSheet)
        self.minType.toggled.connect(self.choiceHandle)
        self.minType.toggled.connect(self.verifyType)

        self.groupType = QtWidgets.QButtonGroup(self)
        self.groupType.addButton(self.maxType)
        self.groupType.addButton(self.minType)

        self.typeError = QtWidgets.QLabel(self)
        self.typeError.setGeometry(50, 330, 600, 30)
        self.typeError.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.typeError.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold))
        self.typeError.setStyleSheet('color: red')

        self.coefficientSection = QtWidgets.QLabel('2.Coefficients of Objective Function', self)
        self.coefficientSection.setGeometry(50, 390, 550, 50)
        self.coefficientSection.setFont(QFont('Microsoft YaHei UI', 22, QFont.Weight.Bold))
        self.coefficientSection.setStyleSheet(self.sectionStyleSheet)

        self.coefficientInput = QtWidgets.QLineEdit(self)
        self.coefficientInput.setFont(QFont('Microsoft YaHei UI', 16, QFont.Weight.Normal))
        self.coefficientInput.setGeometry(50, 480, 600, 40)
        self.coefficientInput.setPlaceholderText('Enter variable coefficients separated by Spaces.')
        self.coefficientInput.setStyleSheet('border: 2px solid #006699')
        self.coefficientInput.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, False)
        self.coefficientInput.textEdited.connect(self.verifyType)
        self.coefficientInput.editingFinished.connect(self.verifyAll)

        self.coefficientError = QtWidgets.QLabel(self)
        self.coefficientError.setGeometry(50, 530, 600, 60)
        self.coefficientError.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.coefficientError.setWordWrap(True)
        self.coefficientError.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold))
        self.coefficientError.setStyleSheet('color: red')

    def choiceHandle(self):
        ChooseErrorHandle(self).handle(self.errorDict)
        radioButton = self.sender()
        if radioButton.isChecked():
            self.parent().objectiveFunctionType = radioButton.text()
            
    def verifyAll(self):
        self.verifyType()
        self.verifyIsCoefficientInput()
        errorNum = ChooseErrorHandle(self).handle(self.errorDict)
        if errorNum == 0:
            self.infoToMatrix.emit(self.coefficientList)
        return errorNum

    def verifyType(self):
        if not (self.maxType.isChecked() or self.minType.isChecked()):
            self.errorDict[1] = True
        else:
            self.errorDict[1] = False
            self.maxType.setStyleSheet(self.typeStyleSheet)
            self.minType.setStyleSheet(self.typeStyleSheet)
            self.typeError.setText(None)
        ChooseErrorHandle(self).handle(self.errorDict)

    def verifyIsCoefficientInput(self):
        if len(self.coefficientInput.text()) == 0:
            self.errorDict[2] = True
        else:
            self.errorDict[2] = False
            self.coefficientInput.setStyleSheet('border: 2px solid #006699')
            self.coefficientError.setText(None)
            self.verifyIsCoefficientInputLegal()
        ChooseErrorHandle(self).handle(self.errorDict)

    def verifyIsCoefficientInputLegal(self):
        inputContent = self.coefficientInput.text()
        if not re.match("^-?[0-9]\d*", inputContent):
            self.errorDict[3] = True
        else:
            self.errorDict[3] = False
            inputContentList = (' '.join(inputContent.split())).split(' ')
            try:
                for elementIndex in range(len(inputContentList)):
                    inputContentList[elementIndex] = int(inputContentList[elementIndex])
            except ValueError:
                self.errorDict[3] = True
            if not self.errorDict[3]:
                self.coefficientError.setText(None)
                self.coefficientInput.setStyleSheet('background-color: white; border: 2px solid #006699')
                self.coefficientList = inputContentList
        ChooseErrorHandle(self).handle(self.errorDict)

    def getResult(self):
        return [self.parent().objectiveFunctionType, self.coefficientList]