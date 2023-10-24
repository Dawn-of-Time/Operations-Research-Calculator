# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

import os
import pandas
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QParallelAnimationGroup, QPoint, QSize
from UI.topBar import TopBar
from UI.Animation.utils import Utils
from Utils.utilsErrorHandle import MatrixErrorHandle

class MatrixWidget(QtWidgets.QWidget): 
    signalToCalculate = pyqtSignal()
    def __init__(self, chooseWidget:QtWidgets.QWidget): 
        super().__init__()
        self.chooseWidget:QtWidgets.QWidget = chooseWidget
        self.addFlag:bool = False
        self.importFlag:bool = False
        self.verifyFlag:bool = True
        self.errorDict:dict = {1:False, 2:False, 3:False, 4:False}
        self.setupUI()

    def setupUI(self):
        self.topBar = TopBar(self)

        self.generateMatrixInfo = QtWidgets.QLabel('Please choose one of the two methods below to generate your matrix, and click the corresponding serial number button.', self)
        self.generateMatrixInfo.setGeometry(50, 60, 600, 50)
        self.generateMatrixInfo.setWordWrap(True)
        self.generateMatrixInfo.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold))

        # Generate Method 1.
        self.generateMethod1 = QtWidgets.QLabel(self)
        self.generateMethod1.setGeometry(50, 120, 525, 100)
        self.generateMethod1ResumeGeometry = self.generateMethod1.geometry()
        self.generateMethod1Layout = QtWidgets.QHBoxLayout()
        self.generateMethod1Layout.setSpacing(0)
        self.generateMethod1Layout.setContentsMargins(0, 0, 0, 0)
        self.generateNum1 = QtWidgets.QPushButton('1')
        self.generateNum1.setFixedSize(75, 100)
        self.generateNum1.setFont(QFont('Microsoft YaHei UI', 22, QFont.Weight.Bold))
        self.generateNum1.setStyleSheet('QPushButton {background-color: #00aacc; border: none; color: white} QPushButton:hover {background-color: #00bbcc} QPushButton:pressed {background-color: #0099cc}')
        self.generateMethod1Introduction = QtWidgets.QLabel()
        self.generateMethod1Introduction.setMinimumHeight(100)
        self.generateMethod1Introduction.setStyleSheet('background-color: #0099cc')
        self.generateMethod1IntroductionLayout = QtWidgets.QVBoxLayout()
        self.generateMethod1IntroductionTitle = QtWidgets.QLabel('Method 1')
        self.generateMethod1IntroductionTitle.setFont(QFont('Microsoft YaHei UI', 15, QFont.Weight.Bold))
        self.generateMethod1IntroductionTitle.setStyleSheet('color: white')
        self.generateMethod1IntroductionContent = QtWidgets.QLabel('Fill in the matrix yourself in the workspace below.')
        self.generateMethod1IntroductionContent.setWordWrap(True)
        self.generateMethod1IntroductionContent.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Light))
        self.generateMethod1IntroductionContent.setStyleSheet('color: white')
        self.generateMethod1IntroductionLayout.addWidget(self.generateMethod1IntroductionTitle, 1)
        self.generateMethod1IntroductionLayout.addWidget(self.generateMethod1IntroductionContent, 3)
        self.generateMethod1Introduction.setLayout(self.generateMethod1IntroductionLayout)
        self.generateMethod1Operation = QtWidgets.QLabel()
        self.generateMethod1Operation.setMinimumHeight(100)
        self.generateMethod1Operation.setStyleSheet('background-color: #0088cc')
        self.generateMethod1OperationLayout = QtWidgets.QVBoxLayout()
        self.generateMethod1OperationTitle = QtWidgets.QLabel('Operation')
        self.generateMethod1OperationTitle.setFont(QFont('Microsoft YaHei UI', 15, QFont.Weight.Bold))
        self.generateMethod1OperationTitle.setStyleSheet('color: white')
        self.lineAdd = QtWidgets.QLabel()
        self.lineAddLayout = QtWidgets.QHBoxLayout()
        self.lineAddLayout.setContentsMargins(0, 0, 0, 0)
        self.lineAddInfo = QtWidgets.QLabel('Line number:', self)
        self.lineAddInfo.setFont(QFont('Microsoft YaHei UI', 10, QFont.Weight.Normal))
        self.lineAddInfo.setStyleSheet('color: white')
        self.lineAddEdit = QtWidgets.QLineEdit()
        self.lineAddEdit.setFont(QFont('Microsoft YaHei UI', 10, QFont.Weight.Light))
        self.lineAddEdit.setStyleSheet('background-color: white')
        self.lineAddButton = QtWidgets.QPushButton('Add')
        self.lineAddButton.setFont(QFont('Microsoft YaHei UI', 10, QFont.Weight.Normal))
        self.lineAddButton.setFixedSize(50, 20)
        self.lineAddButton.setStyleSheet('QPushButton {background-color: #0077cc; color: white; border: 1px solid white} QPushButton:hover {background-color: #00bbcc} QPushButton:pressed {background-color: #0066cc}')
        self.lineAddLayout.addWidget(self.lineAddInfo, 1)
        self.lineAddLayout.addWidget(self.lineAddEdit, 2)
        self.lineAddLayout.addWidget(self.lineAddButton, 2)
        self.lineAdd.setLayout(self.lineAddLayout)
        self.lineAddErrorInfo = QtWidgets.QLabel()
        self.lineAddErrorInfo.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lineAddErrorInfo.setWordWrap(True)
        self.lineAddErrorInfo.setFont(QFont('Microsoft YaHei UI', 8, QFont.Weight.Bold))
        self.lineAddErrorInfo.setStyleSheet('color: #ffcccc')
        self.generateMethod1OperationLayout.addWidget(self.generateMethod1OperationTitle, 1)
        self.generateMethod1OperationLayout.addWidget(self.lineAdd, 3)
        self.generateMethod1OperationLayout.addWidget(self.lineAddErrorInfo, 1)
        self.generateMethod1OperationLayout.setContentsMargins(5, 5, 5, 5)
        self.generateMethod1Operation.setLayout(self.generateMethod1OperationLayout)
        self.generateMethod1Layout.addWidget(self.generateNum1, 1)
        self.generateMethod1Layout.addWidget(self.generateMethod1Introduction, 3)
        self.generateMethod1Layout.addWidget(self.generateMethod1Operation, 3)
        self.generateMethod1.setLayout(self.generateMethod1Layout)

        self.cover1 = QtWidgets.QLabel(self)
        self.cover1.setStyleSheet('background-color: white')
        self.cover1.setGeometry(350, 120, 30, 100)

        # Generate Method 2.
        self.generateMethod2 = QtWidgets.QLabel(self)
        self.generateMethod2.setGeometry(380, 120, 525, 100)
        self.generateMethod2ResumeGeometry = self.generateMethod2.geometry()
        self.generateMethod2Layout = QtWidgets.QHBoxLayout()
        self.generateMethod2Layout.setSpacing(0)
        self.generateMethod2Layout.setContentsMargins(0, 0, 0, 0)
        self.generateNum2 = QtWidgets.QPushButton('2')
        self.generateNum2.setFixedSize(75, 100)
        self.generateNum2.setFont(QFont('Microsoft YaHei UI', 22, QFont.Weight.Bold))
        self.generateNum2.setStyleSheet('QPushButton {background-color: #00aacc; border: none; color: white} QPushButton:hover {background-color: #00bbcc} QPushButton:pressed {background-color: #0099cc}')
        self.generateMethod2Introduction = QtWidgets.QLabel()
        self.generateMethod2Introduction.setMinimumHeight(100)
        self.generateMethod2Introduction.setStyleSheet('background-color: #0088cc')
        self.generateMethod2IntroductionLayout = QtWidgets.QVBoxLayout()
        self.generateMethod2IntroductionTitle = QtWidgets.QLabel('Method 2')
        self.generateMethod2IntroductionTitle.setFont(QFont('Microsoft YaHei UI', 15, QFont.Weight.Bold))
        self.generateMethod2IntroductionTitle.setStyleSheet('color: white')
        self.generateMethod2IntroductionContent = QtWidgets.QLabel('Import your matrix through Excel.')
        self.generateMethod2IntroductionContent.setWordWrap(True)
        self.generateMethod2IntroductionContent.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Light))
        self.generateMethod2IntroductionContent.setStyleSheet('color: white')
        self.generateMethod2IntroductionLayout.addWidget(self.generateMethod2IntroductionTitle, 1)
        self.generateMethod2IntroductionLayout.addWidget(self.generateMethod2IntroductionContent, 3)
        self.generateMethod2Introduction.setLayout(self.generateMethod2IntroductionLayout)
        self.generateMethod2Operation = QtWidgets.QLabel()
        self.generateMethod2Operation.setMinimumHeight(100)
        self.generateMethod2Operation.setStyleSheet('background-color: #0099cc')
        self.generateMethod2OperationLayout = QtWidgets.QVBoxLayout()
        self.generateMethod2OperationTitle = QtWidgets.QLabel('Operation')
        self.generateMethod2OperationTitle.setFont(QFont('Microsoft YaHei UI', 15, QFont.Weight.Bold))
        self.generateMethod2OperationTitle.setStyleSheet('color: white')
        self.importButton = QtWidgets.QPushButton('Import')
        self.importButton.setFont(QFont('Microsoft YaHei UI', 10, QFont.Weight.Normal))
        self.importButton.setFixedHeight(25)
        self.importButton.setStyleSheet('QPushButton {background-color: #0077cc; color: white; border: 1px solid white} QPushButton:hover {background-color: #00bbcc} QPushButton:pressed {background-color: #0066cc}')
        self.importErrorInfo = QtWidgets.QLabel()
        self.importErrorInfo.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.importErrorInfo.setWordWrap(True)
        self.importErrorInfo.setFont(QFont('Microsoft YaHei UI', 8, QFont.Weight.Bold))
        self.importErrorInfo.setStyleSheet('color: #ffcccc')
        self.generateMethod2OperationLayout.addWidget(self.generateMethod2OperationTitle, 1)
        self.generateMethod2OperationLayout.addWidget(self.importButton, 3)
        self.generateMethod2OperationLayout.addWidget(self.importErrorInfo, 1)
        self.generateMethod2OperationLayout.setContentsMargins(5, 5, 5, 5)
        self.generateMethod2Operation.setLayout(self.generateMethod2OperationLayout)
        self.generateMethod2Layout.addWidget(self.generateNum2, 1)
        self.generateMethod2Layout.addWidget(self.generateMethod2Introduction, 3)
        self.generateMethod2Layout.addWidget(self.generateMethod2Operation, 3)
        self.generateMethod2.setLayout(self.generateMethod2Layout)

        self.cover2 = QtWidgets.QLabel(self)
        self.cover2.setStyleSheet('background-color: white')
        self.cover2.setGeometry(680, 120, 58, 100)

        self.workspaceTitle = QtWidgets.QLabel('Workspace', self)
        self.workspaceTitle.setGeometry(50, 240, 100, 20)
        self.workspaceTitle.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold))

        self.workspaceErrorInfo = QtWidgets.QLabel(self)
        self.workspaceErrorInfo.setGeometry(150, 240, 250, 20)
        self.workspaceErrorInfo.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold))
        self.workspaceErrorInfo.setStyleSheet('color: red')

        self.chooseWidget.infoToMatrix.connect(self.initWorkspace)
        self.generateNum1.clicked.connect(self.isWorkspaceAddedOrImported)
        self.lineAddEdit.editingFinished.connect(self.verifyLineAddEdit)
        self.generateNum2.clicked.connect(self.isWorkspaceAddedOrImported)
        self.lineAddButton.clicked.connect(self.verifyLineAddEdit)
        self.importButton.clicked.connect(self.verifyImport)

    def initWorkspace(self, coefficientList:list) -> None:
        self.variableNum:int = len(coefficientList)
        self.workspace = QtWidgets.QTableWidget(2, self.variableNum + 2, self)
        self.workspace.setGeometry(50, 280, 630, 350)
        self.workspace.horizontalHeader().setVisible(False)
        self.workspace.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.workspace.itemChanged.connect(self.verifyWorkspace)
        for rowIndex in range(2):
            for columnIndex in range(self.variableNum + 2):
                self.workspace.setCellWidget(rowIndex, columnIndex, QtWidgets.QLabel(''))
        for variableIndex in range(self.variableNum):
            item = QtWidgets.QLabel()
            itemLayout = QtWidgets.QHBoxLayout()
            itemLayout.setSpacing(0)
            itemLayout.setContentsMargins(20, 0, 20, 0)
            itemVariable = QtWidgets.QLabel(f'<i>x</i><sub>{variableIndex + 1}</sub>')
            itemVariable.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
            itemVariable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            itemConstraint = QtWidgets.QComboBox()
            itemConstraint.addItem("≥ 0")
            itemConstraint.addItem("≤ 0")
            itemConstraint.addItem("= 0")
            itemConstraint.addItem("Unrestraint")
            itemConstraint.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
            itemLayout.addWidget(itemVariable, 1)
            itemLayout.addWidget(itemConstraint, 1)
            item.setLayout(itemLayout)
            self.workspace.setCellWidget(0, variableIndex, item)
            coefficient = QtWidgets.QLabel(str(coefficientList[variableIndex]))
            coefficient.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
            coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.workspace.setCellWidget(1, variableIndex, coefficient)
        comparision = QtWidgets.QLabel('<i>Comparison</i>')
        comparision.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
        comparision.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workspace.setCellWidget(0, self.variableNum, comparision)
        resource = QtWidgets.QLabel('<i>b</i>')
        resource.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
        resource.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workspace.setCellWidget(0, self.variableNum + 1, resource)
        self.workspace.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(''))
        coefficientItem = QtWidgets.QTableWidgetItem('C')
        coefficientItem.setFont(QFont('Microsoft YaHei UI', 12, QFont.Weight.Light))
        coefficientItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workspace.setVerticalHeaderItem(1, coefficientItem)
        
    def isWorkspaceAddedOrImported(self):
        button = self.sender()
        if self.addFlag or self.importFlag:
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle('Change the method?')
            dialog.setFixedSize(420, 200)
            info = QtWidgets.QLabel('Are you sure you want to change the method?', dialog)
            info.setGeometry(20, 20, 380, 50)
            info.setFont((QFont('Microsoft YaHei UI', 12, QFont.Weight.Bold)))
            info.setWordWrap(True)
            subInfo = QtWidgets.QLabel('This will cause you to lose what you have already edited.', dialog)
            subInfo.setGeometry(20, 70, 380, 50)
            subInfo.setFont((QFont('Microsoft YaHei UI', 10, QFont.Weight.Normal)))
            subInfo.setWordWrap(True)
            buttonStyle = 'QPushButton {background-color: #00cccc;border: none} QPushButton:hover {background-color: #00ccff} QPushButton:pressed {background-color: #00bbff}'
            cancelButton = QtWidgets.QPushButton(dialog)
            cancelButton.setGeometry(0, 150, 210, 50)
            cancelButton.setStyleSheet(buttonStyle)
            cancelButton.setIcon(QIcon('res/icon/cancel.png'))
            cancelButton.setIconSize(QSize(20, 20))
            OKButton = QtWidgets.QPushButton(dialog)
            OKButton.setGeometry(210, 150, 210, 50)
            OKButton.setStyleSheet(buttonStyle)
            OKButton.setIcon(QIcon('res/icon/ok.png'))
            OKButton.setIconSize(QSize(20, 20))
            dialog.show()
            cancelButton.clicked.connect(dialog.close)
            OKButton.clicked.connect(dialog.close)
            OKButton.clicked.connect(self.cleanWorkspace)
            OKButton.clicked.connect(lambda: self.updateMethod(button))
        else:
            self.updateMethod()

    def updateMethod(self, button = None):
        self.errorDict = {1:False, 2:False, 3:False, 4:False}
        MatrixErrorHandle(self).handle(self.errorDict)
        if button == None:
            button = self.sender()
        if button == self.generateNum1:
            self.lineAddEdit.setText(None)
            self.lineAddEdit.setStyleSheet('background-color: white')
            self.lineAddErrorInfo.setText(None)
        else:
            self.importErrorInfo.setText(None)
        parallelGroup = QParallelAnimationGroup(self)
        if button == self.generateNum1:
            shiftAnimation1 = Utils(self.cover1, self).shift(QPoint(self.cover1.x(), self.cover1.y()), QPoint(575, 120), 300)
            shiftAnimation2 = Utils(self.generateMethod2, self).shift(QPoint(self.generateMethod2.x(), self.generateMethod2.y()), QPoint(605, 120), 300)
        else:
            shiftAnimation1 = Utils(self.cover1, self).shift(QPoint(self.cover1.x(), self.cover1.y()), QPoint(125, 120), 300)
            shiftAnimation2 = Utils(self.generateMethod2, self).shift(QPoint(self.generateMethod2.x(), self.generateMethod2.y()), QPoint(155, 120), 300)
        parallelGroup.addAnimation(shiftAnimation1)
        parallelGroup.addAnimation(shiftAnimation2)
        parallelGroup.start()

    def addLine(self):
        column_num = self.variableNum + 2
        rowNum = self.workspace.rowCount()
        self.workspace.insertRow(rowNum)
        serialNum = rowNum - 1
        serialNumItem = QtWidgets.QTableWidgetItem(str(serialNum))
        serialNumItem.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
        serialNumItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workspace.setVerticalHeaderItem(rowNum, serialNumItem)
        for columnIndex in range(column_num):
            if columnIndex == column_num - 2:
                choice = QtWidgets.QComboBox(self)
                choice.addItem("≤")
                choice.addItem("≥")
                choice.addItem("=")
                choice.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                self.workspace.setCellWidget(rowNum, columnIndex, choice)
            else:
                unit_input = QtWidgets.QTableWidgetItem()
                unit_input.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                unit_input.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.workspace.setItem(rowNum, columnIndex, unit_input)
    
    def addNullLines(self, addNumber:int):
        self.addFlag = True
        self.verifyFlag = False
        for lineIndex in range(addNumber):
            self.addLine()
        self.verifyFlag = True
        self.lineAddEdit.setText(None)

    def cleanWorkspace(self):
        rowNum = self.workspace.rowCount()
        for rowIndex in range(rowNum - 1, 1, -1):
            self.workspace.removeRow(rowIndex)
        self.addFlag = False
        self.importFlag = False
        self.errorDict[4] = False
        self.workspaceErrorInfo.setText(None)

    def verifyImport(self):
        filePath, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a file to import', os.getcwd(), "Excel Files(*.xlsx *.xls)")
        if len(filePath) == 0:
            return
        self.excelList = pandas.read_excel(filePath, keep_default_na=False, header=None).values.tolist()
        self.columnNum = len(self.excelList[0])
        if self.columnNum != self.variableNum + 2:
            self.errorDict[2] = True
        else:
            self.errorDict[2] = False
            self.importErrorInfo.setText(None)
            self.verifyImportData()
        MatrixErrorHandle(self).handle(self.errorDict)

    def verifyImportData(self):
        rowNum = len(self.excelList)
        for rowIndex in range(0, rowNum):
            for columnIndex in range(self.columnNum):
                if columnIndex == self.columnNum - 2:
                    choice = self.excelList[rowIndex][columnIndex]
                    if choice not in ['more', 'less', 'equal']:
                        self.errorDict[3] = True
                        return
                    else:
                        self.errorDict[3] = False
                        self.importErrorInfo.setText(None)
                else:
                    if type(self.excelList[rowIndex][columnIndex]) != int and self.excelList[rowIndex][columnIndex] != '':
                        self.errorDict[3] = True
                        return
                    self.errorDict[3] = False
                    self.importErrorInfo.setText(None)
        MatrixErrorHandle(self).handle(self.errorDict)
        self.importExcel()

    def importExcel(self):
        self.verifyFlag = False
        rowNum = len(self.excelList)
        for rowIndex in range(rowNum):
            self.addLine()
        rowNum = self.workspace.rowCount()
        for rowIndex in range(2, rowNum):
            for columnIndex in range(self.columnNum):
                if columnIndex == self.columnNum - 2:
                    choice = self.excelList[rowIndex - 2][columnIndex]
                    if choice == 'less':
                        self.workspace.cellWidget(rowIndex, columnIndex).setCurrentIndex(0)
                    elif choice == 'more':
                        self.workspace.cellWidget(rowIndex, columnIndex).setCurrentIndex(1)
                    elif choice == 'equal':
                        self.workspace.cellWidget(rowIndex, columnIndex).setCurrentIndex(2)
                else:
                    self.workspace.item(rowIndex, columnIndex).setText(str(self.excelList[rowIndex - 2][columnIndex]))
        self.verifyFlag = True
        self.importFlag = True

    def verifyLineAddEdit(self):
        try:
            addNumber = int(self.lineAddEdit.text())
            if addNumber < 0:
                raise ValueError
            else:
                self.errorDict[1] = False
                self.lineAddEdit.setStyleSheet('background-color: white')
                self.lineAddErrorInfo.setText(None)
                if self.sender() == self.lineAddButton:
                    self.addNullLines(addNumber)
        except ValueError:
            self.errorDict[1] = True
        MatrixErrorHandle(self).handle(self.errorDict)

    def verifyWorkspace(self):
        if self.verifyFlag:
            rowNum = self.workspace.rowCount()
            columnNum = self.variableNum + 2
            for rowIndex in range(2, rowNum):
                for columnIndex in range(0, columnNum):
                    if columnIndex != columnNum - 2:
                        item = self.workspace.item(rowIndex, columnIndex).text()
                        if len(item) != 0:
                            try:
                                int(item)
                            except ValueError:
                                self.errorDict[4] = True
                                MatrixErrorHandle(self).handle(self.errorDict)
                                return
        self.errorDict[4] = False
        self.workspaceErrorInfo.setText(None)
        errorNum = MatrixErrorHandle(self).handle(self.errorDict)
        return errorNum
    
    def verifyAll(self):
        errorNum = self.verifyWorkspace()
        if errorNum == 0:
            self.signalToCalculate.emit()
        return errorNum

    def getResult(self) ->list:
        rowNum = self.workspace.rowCount()
        columnNum = self.variableNum + 2
        finalMatrix = []
        variableConstraintList = []
        for columnIndex in range(self.variableNum):
            item = self.workspace.cellWidget(0, columnIndex).findChild(QtWidgets.QComboBox)
            data = item.currentText()
            if data == "≤ 0":
                data = 'less'
            elif data == "≥ 0":
                data = 'more'
            elif data == "= 0":
                data = 'equal'
            elif data == 'Unrestraint':
                data = 'Unrestraint'
            variableConstraintList.append(data)
        for lineIndex in range(2, rowNum):
            line = []
            for columnIndex in range(columnNum):
                if columnIndex == columnNum - 2:
                    item = self.workspace.cellWidget(lineIndex, columnIndex)
                    data = item.currentText()
                    if data == "≤":
                        data = 'less'
                    elif data == "≥":
                        data = 'more'
                    elif data == "=":
                        data = 'equal'
                else:
                    item = self.workspace.item(lineIndex, columnIndex)
                    data = item.text()
                    if len(data) == 0:
                        data = 0
                    else:
                        data = int(data)                          
                line.append(data)
            finalMatrix.append(line)
        return [variableConstraintList, finalMatrix]