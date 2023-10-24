# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

from calculate.calculate import Calculate
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QFont, QIcon
# from PyQt6.QtPrintSupport import QPrintDialog
from PyQt6.QtCore import Qt
from UI.topBar import TopBar

class CalculateWidget(QtWidgets.QWidget): 
    def __init__(self, chooseWidget, matrixWidget): 
        super().__init__()
        self.topBar = TopBar(self)
        self.topBar.continueButton.setIcon(QIcon())
        self.topBar.continueButton.setEnabled(False)
        self.chooseWidget = chooseWidget
        self.matrixWidget = matrixWidget
        self.matrixWidget.signalToCalculate.connect(self.calculate)
        self.setupUI()

    def setupUI(self):
        self.resultTitle = QtWidgets.QLabel(self)
        self.resultTitle.setGeometry(50, 50, 400, 50)
        self.resultTitle.setFont(QFont('Microsoft YaHei UI', 15, QFont.Weight.Bold))
        # self.exportButton = QtWidgets.QPushButton('Export to PDF', self)
        # self.exportButton.setGeometry(538, 50, 100, 30)
        # self.exportButton.setStyleSheet('QPushButton {background-color: #0077cc; color: white; border: 1px solid white} QPushButton:hover {background-color: #00bbcc} QPushButton:pressed {background-color: #0066cc}')
        # self.exportButton.clicked.connect(self.export)

    def calculate(self):
        # Get the necessary parameters.
        chooseResult = self.chooseWidget.getResult()
        matrixResult = self.matrixWidget.getResult()
        objectiveFunctionType = chooseResult[0]
        coefficientList = chooseResult[1]
        variableConstraintList = matrixResult[0]
        finalMatrix = matrixResult[1]

        # Calculate.
        result = Calculate().calculate(objectiveFunctionType, coefficientList, variableConstraintList, finalMatrix)

        # Show.
        self.updateResultSpace(result)

    def updateResultSpace(self, result):
        result1 = result[0] # Stage 1 result.
        result2 = result[1] # Stage 2 result.
        resultFlag = result[2]
        self.resultTitle.setText(resultFlag)
        self.resultSpace = QtWidgets.QTableWidget(0, 0, self)
        self.resultSpace.setGeometry(50, 100, 638, 500)
        self.resultSpace.horizontalHeader().setVisible(False)
        self.resultSpace.verticalHeader().setVisible(False)
        self.resultSpace.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # If the result1 is empty, the two-stage method is not being used.
        stage1Flag = False
        foreRowNum = 0 # Records the number of rows before updateUI.
        if len(result1) != 0: 
            stage1Flag = True 
            for columnIndex in range(len(result1[0]) + 2):
                self.resultSpace.insertColumn(self.resultSpace.columnCount())
            # UI.
            stageTitle = QtWidgets.QLabel('Stage 1')
            stageTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
            stageTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.resultSpace.insertRow(self.resultSpace.rowCount())
            self.resultSpace.setCellWidget(0, 0, stageTitle)
            foreRowNum += 1
            self.updateUI(result1, foreRowNum)
            # Add a blank row if the resultFlag of Stage 1 is not 'Infeasibility Solution'.
            if resultFlag != 'Infeasibility Solution':
                self.resultSpace.insertRow(self.resultSpace.rowCount())
                foreRowNum = self.resultSpace.rowCount()

        if len(result2) != 0:
            if stage1Flag:
                # The number of columns in Stage 1 must be greater than in Stage 2, so columns need not be added.
                stageTitle = QtWidgets.QLabel('Stage 2')
                stageTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
                stageTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.resultSpace.insertRow(self.resultSpace.rowCount())
                self.resultSpace.setCellWidget(self.resultSpace.rowCount() - 1, 0, stageTitle)
                # update foreRowNum.
                foreRowNum += 1
            else:
                for columnIndex in range(len(result2[0]) + 2):
                    self.resultSpace.insertColumn(self.resultSpace.columnCount())
            self.updateUI(result2, foreRowNum)

        # Set the table unclickable.
        self.resultSpace.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    
    def updateUI(self, resultPartial:list, foreRowNum:int = 0):
        coefficientList:list = resultPartial[0]
        unitIndexNum:int = len(resultPartial[1])
        coefficientTitle = QtWidgets.QLabel('<i>c<sub>j</sub></i>')
        coefficientTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
        coefficientTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultSpace.insertRow(self.resultSpace.rowCount())
        self.resultSpace.setCellWidget(foreRowNum, 1, coefficientTitle)

        for coefficientIndex in range(1, len(coefficientList)):
            coefficient = QtWidgets.QLabel(str(coefficientList[coefficientIndex]))
            coefficient.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
            coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.resultSpace.setCellWidget(foreRowNum, coefficientIndex + 2, coefficient)

        baseCoefficientTitle = QtWidgets.QLabel('<i>C<sub>B</sub></i>')
        baseCoefficientTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
        baseCoefficientTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultSpace.insertRow(self.resultSpace.rowCount())
        self.resultSpace.setCellWidget(foreRowNum + 1, 0, baseCoefficientTitle)

        baseTitle = QtWidgets.QLabel('Base')
        baseTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
        baseTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultSpace.setCellWidget(foreRowNum + 1, 1, baseTitle)

        resourceTitle = QtWidgets.QLabel('<i>b</i>')
        resourceTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Bold))
        resourceTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultSpace.setCellWidget(foreRowNum + 1, 2, resourceTitle)

        for columnIndex in range(3, len(coefficientList) + 2):
            variable = QtWidgets.QLabel('<i>x</i><sub>' + str(columnIndex - 2) + '</sub>')
            variable.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
            variable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.resultSpace.setCellWidget(foreRowNum + 1, columnIndex, variable)
        
        index = 1
        iterateTime = 0
        while index < len(resultPartial):
            if index % 3 == 1:
                unitIndexList = resultPartial[index]
                for rowIndex in range(len(unitIndexList) + 1):
                    self.resultSpace.insertRow(self.resultSpace.rowCount())
                for unitIndexIndex in range(unitIndexNum):
                    baseCoefficient = QtWidgets.QLabel(str(coefficientList[unitIndexList[unitIndexIndex]]))
                    baseCoefficient.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                    baseCoefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.resultSpace.setCellWidget(foreRowNum + 2 + iterateTime * (unitIndexNum + 1) + unitIndexIndex, 0, baseCoefficient)
                    baseVariable = QtWidgets.QLabel('<i>x</i><sub>' + str(unitIndexList[unitIndexIndex]) + '</sub>')
                    baseVariable.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                    baseVariable.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.resultSpace.setCellWidget(foreRowNum + 2 + iterateTime * (unitIndexNum + 1) + unitIndexIndex, 1, baseVariable)
            elif index % 3 == 2:
                finalMatrix = resultPartial[index]
                rowNum = len(finalMatrix)
                columnNum = len(finalMatrix[0])
                for rowIndex in range(rowNum):
                    for columnIndex in range(columnNum):
                        data = str(finalMatrix[rowIndex][columnIndex])
                        item = QtWidgets.QLabel(data)
                        item.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                        item.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.resultSpace.setCellWidget(foreRowNum + 2 + iterateTime * (rowNum + 1) + rowIndex, 2 + columnIndex, item)
            elif index % 3 == 0:
                checkingList = resultPartial[index]
                checkingListTitle = QtWidgets.QLabel('<i>&sigma;<sub>j</sub></i>')
                checkingListTitle.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                checkingListTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.resultSpace.setCellWidget(self.resultSpace.rowCount() - 1, 1, checkingListTitle)
                for checkingIndex in range(1, len(checkingList)):
                    checkingNumber = QtWidgets.QLabel(str(checkingList[checkingIndex]))
                    checkingNumber.setFont(QFont('Times New Roman', 12, QFont.Weight.Normal))
                    checkingNumber.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.resultSpace.setCellWidget(self.resultSpace.rowCount() - 1, 2 + checkingIndex, checkingNumber)
                iterateTime += 1
            index += 1

    # TODO: At present, it is difficult to find a suitable way to export PDF files.
    # def export(self):
    #     filePath, fileType =QtWidgets.QFileDialog.getSaveFileName(self, "Export to PDF", "OR result", "PDF Files (*.pdf)")
    #     if len(filePath) == 0:
    #         return