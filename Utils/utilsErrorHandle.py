# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
class UtilsErrorHandle():
    def __init__(self) -> None:
        pass

class ChooseErrorHandle(UtilsErrorHandle):
    def __init__(self, parent) -> None:
        super().__init__()
        self.__parent = parent

    def handle(self, errorDict:dict):
        errorNum = 0
        for key, value in errorDict.items():
            if value:
                errorFlag = key
                if errorFlag == 1:
                    typeErrorStyleSheet = 'background-color: #ffcccc; padding: 0px 30px; border-left: 10px solid #ff0000; border-top: 1px solid #ff0000; border-bottom: 1px solid #ff0000; border-right: 1px solid #ff0000;'
                    self.__parent.maxType.setStyleSheet(typeErrorStyleSheet)
                    self.__parent.minType.setStyleSheet(typeErrorStyleSheet)
                    self.__parent.typeError.setText('Make sure you select one of the two options above.')
                elif errorFlag == 2:
                    coefficientInputErrorStyleSheet = 'background-color: #ffcccc; border: 2px solid #ff0000'
                    self.__parent.coefficientInput.setStyleSheet(coefficientInputErrorStyleSheet)
                    self.__parent.coefficientError.setText('Please enter the coefficient(s) in the input field above.')
                elif errorFlag == 3:
                    coefficientInputErrorStyleSheet = 'background-color: #ffcccc; border: 2px solid #ff0000'
                    self.__parent.coefficientInput.setStyleSheet(coefficientInputErrorStyleSheet)
                    self.__parent.coefficientError.setText('Only integer coefficients are supported, and please separate them with Spaces.')
                errorNum += 1
        if errorNum != 0:
            self.__parent.topBar.infoButton.setStyleSheet('QPushButton {background-color: #ff5555;border: none;color: white;} QPushButton:hover {background-color: #ff7777} QPushButton:pressed {background-color: #ff6677}')
            self.__parent.topBar.infoButton.setFont(QFont('Microsoft YaHei UI', 14, QFont.Weight.Normal))
            self.__parent.topBar.infoButton.setIcon(QIcon('res/icon/error.png'))
            self.__parent.topBar.infoButton.setIconSize(QSize(20, 20))
            if errorNum == 1:
                self.__parent.topBar.infoButton.setText('1 error has occurred')
            else:
                self.__parent.topBar.infoButton.setText(str(errorNum) + ' errors have occurred')
        if errorNum == 0:
            self.__parent.topBar.infoButtonResume()
        return errorNum
    
class MatrixErrorHandle(UtilsErrorHandle):
    def __init__(self, parent) -> None:
        super().__init__()
        self.__parent = parent

    def handle(self, errorDict:dict):
        errorNum = 0
        for key, value in errorDict.items():
            if value:
                errorFlag = key
                if errorFlag == 1:
                    typeErrorStyleSheet = 'background-color: #ffcccc'
                    self.__parent.lineAddEdit.setStyleSheet(typeErrorStyleSheet)
                    self.__parent.lineAddErrorInfo.setText('Must be a positive integer.')
                elif errorFlag == 2:
                    columnNum = self.__parent.columnNum
                    text = 'The number of excel columns (' + str(columnNum) + ') does not match.'
                    if columnNum >= 10000:
                        text = 'The number of columns (M) does not match.(M>=10000)'
                    self.__parent.importErrorInfo.setText(text)
                elif errorFlag == 3:
                    self.__parent.importErrorInfo.setText('The data does not conform to the rules.')
                elif errorFlag == 4:
                    self.__parent.workspaceErrorInfo.setText('Only integers are supported.')
                errorNum += 1
        if errorNum != 0:
            self.__parent.topBar.infoButton.setStyleSheet('QPushButton {background-color: #ff5555;border: none;color: white;} QPushButton:hover {background-color: #ff7777} QPushButton:pressed {background-color: #ff6677}')
            self.__parent.topBar.infoButton.setFont(QFont('Microsoft YaHei UI', 14, QFont.Weight.Normal))
            self.__parent.topBar.infoButton.setIcon(QIcon('res/icon/error.png'))
            self.__parent.topBar.infoButton.setIconSize(QSize(20, 20))
            if errorNum == 1:
                self.__parent.topBar.infoButton.setText('1 error has occurred')
            else:
                self.__parent.topBar.infoButton.setText(str(errorNum) + ' errors have occurred')
        if errorNum == 0:
            self.__parent.topBar.infoButtonResume()
        return errorNum