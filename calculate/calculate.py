# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  
import Utils.utilsCalculate as utils
import copy
class Calculate():
    def __init__(self) -> None:
        self.resultFlag = ''

    def calculate(self, objectiveFunctionType:str, coefficientList:list, variableConstraintList:list, finalMatrix:list):
        self.finalMatrix = finalMatrix
        self.coefficientList = coefficientList
        variableNum = len(self.coefficientList)
        self.coefficientList = [0] + self.coefficientList
        variableConstraintList = [0] + variableConstraintList
        rowNum = len(self.finalMatrix)
        columnNum = len(self.finalMatrix[0])
        self.result1 = []
        self.result2 = []
        # Step 1: Turn 'min' to 'max'.
        if objectiveFunctionType == "min":
            for coefficientIndex in range(len(self.coefficientList)):
                self.coefficientList[coefficientIndex] *= -1
            objectiveFunctionType == "max"

        # Step 2: Put the resource in the first column, and change the matrix according to some rules.
        addUnitVectorList = []
        for rowIndex in range(rowNum):
            for columnIndex in range(columnNum - 1):
                utils.swap(self.finalMatrix[rowIndex], -columnIndex - 1, -columnIndex - 2)
            # Check whether the penult element  (resource)  per line is less than 0. If so, multiply the line by -1.
            if self.finalMatrix[rowIndex][0] < 0:
                for columnIndex in range(columnNum - 1):
                    self.finalMatrix[rowIndex][columnIndex] *= -1
                # The inequality changes because the it is multiplied by -1.
                if self.finalMatrix[rowIndex][-1] == 'less':
                    self.finalMatrix[rowIndex][-1] == 'more'
                elif self.finalMatrix[rowIndex][-1] == 'more':
                    self.finalMatrix[rowIndex][-1] == 'less'
            # Convert inequalities into equations through adding some variables.
            if self.finalMatrix[rowIndex][-1] != 'equal':
                # For 'less', add slack variables. For 'more', add surplus variables. The value coefficient of them are 0.
                self.coefficientList.append(0)
                # Both of them need a column to be added to the final matrix.
                addUnitVector = [0] * rowNum
                if self.finalMatrix[rowIndex][-1] == 'less':
                    addUnitVector[rowIndex] = 1
                elif self.finalMatrix[rowIndex][-1] == 'more':
                    addUnitVector[rowIndex] = -1    
                addUnitVectorList.append(addUnitVector)
            # The last element is (or is changed to) 'equal', and there is no need to keep it.
            self.finalMatrix[rowIndex].pop()
            # Deal with variables which are unrestraint or less than 0.
            for variableConstraintIndex in range(len(variableConstraintList)):
                if variableConstraintList[variableConstraintIndex] == "Unrestraint":
                    addUnitVector = []
                    for rowIndex in range(rowNum):
                        addUnitVector.append(self.finalMatrix[rowIndex][variableConstraintIndex] * (-1))
                    self.coefficientList.append(self.coefficientList[variableConstraintIndex])
                    addUnitVectorList.append(addUnitVector)
                elif variableConstraintList[variableConstraintIndex] == "less":
                    self.coefficientList[variableConstraintIndex] *= (-1)
                    for rowIndex in range(rowNum):
                        self.finalMatrix[rowIndex][variableConstraintIndex] *= (-1)
        if len(addUnitVectorList) != 0:
            for addUnitVectorIndex in range(len(addUnitVectorList)):
                utils.addColumn(self.finalMatrix, addUnitVectorList[addUnitVectorIndex])

        # Step 3: Find the basic feasible solution. (Initial)
        # Find the unit matrix.
        self.unitIndexList = utils.findUnitMatrix(self.finalMatrix)
        # If there is no unit matrix, add artificial variables.
        artificialVariableNum = 0
        artificialVariableIndexList = []
        if -1 in self.unitIndexList:
            addUnitMatrix = []
            for unit_index_index in range(len(self.unitIndexList)):
                if self.unitIndexList[unit_index_index] == -1:
                    # Add artificial variables.
                    addUnitVector = [0] * rowNum
                    addUnitVector[unit_index_index] = 1
                    addUnitMatrix.append(addUnitVector)
                    artificialVariableIndexList.append(len(self.finalMatrix[0]) + len(addUnitMatrix) - 1) # Mark the artificial variable column.
                    artificialVariableNum += 1
            if len(addUnitMatrix) != 0:
                for addUnitVectorIndex in range(len(addUnitMatrix)):
                    self.finalMatrix = utils.addColumn(self.finalMatrix, addUnitMatrix[addUnitVectorIndex])
            newCoefficientList = [0] * (len(self.finalMatrix[0]))
            for artificialVariableIndex in artificialVariableIndexList:
                newCoefficientList[artificialVariableIndex] = -1
            self.unitIndexList = utils.findUnitMatrix(self.finalMatrix)
        # Step 3.1: First stage.
        self.stage1Flag = False
        if artificialVariableNum != 0:
            self.stage1Flag = True
            self.iterate(newCoefficientList)
            for artificialVariableIndex in artificialVariableIndexList:
                if artificialVariableIndex in self.unitIndexList and len(self.resultFlag) == 0:
                    self.resultFlag = 'Infeasibility Solution'
                    return [self.result1, self.result2, self.resultFlag]
            for line in self.finalMatrix:
                for count in range(artificialVariableNum):
                    line.pop()
        self.stage1Flag = False
        # Step 3.2: Second stage.(General steps)
        if len(self.resultFlag) == 0:
            self.iterate(self.coefficientList)
        return [self.result1, self.result2, self.resultFlag]

    def iterate(self, coefficientList):
        iterate_time = 1
        checkingList = utils.getCheckingNumber(coefficientList, self.unitIndexList, self.finalMatrix)
        if self.stage1Flag:
            self.result1.append(coefficientList.copy())
            self.result1.append(self.unitIndexList.copy())
            self.result1.append(copy.deepcopy(self.finalMatrix))
            self.result1.append(checkingList.copy())
        else:
            self.result2.append(coefficientList.copy())
            self.result2.append(self.unitIndexList.copy())
            self.result2.append(copy.deepcopy(self.finalMatrix))
            self.result2.append(checkingList.copy())
        while utils.checkout(checkingList) == False:
            iterate_time += 1
            # Iterate.
            # Determine the variable which should be swapped into the base.
            # Find the first positive number in the list.(Bland)
            for checkingNumberIndex in range(1, len(checkingList[1:])): # The value at index 0 is not valid.
                if checkingList[checkingNumberIndex] > 0:
                    swapNonBasicVariableIndex = checkingNumberIndex
                    break
            swapBasicVariableIndex = utils.findSwapBasicVariableIndex(self.finalMatrix, swapNonBasicVariableIndex, self.unitIndexList)
            if swapBasicVariableIndex == -1:
                self.resultFlag = "Unbounded Solution"
                return
            self.unitIndexList[swapBasicVariableIndex] = swapNonBasicVariableIndex
            # Gauss transform -> new unit matrix.
            self.finalMatrix = utils.transformToUnitMatrix(self.finalMatrix, swapNonBasicVariableIndex, swapBasicVariableIndex)
            self.unitIndexList[swapBasicVariableIndex] = swapNonBasicVariableIndex     
            checkingList = utils.getCheckingNumber(coefficientList, self.unitIndexList, self.finalMatrix)
            if self.stage1Flag:
                self.result1.append(self.unitIndexList.copy())
                self.result1.append(copy.deepcopy(self.finalMatrix))
                self.result1.append(checkingList.copy())
            else:
                self.result2.append(self.unitIndexList.copy())
                self.result2.append(copy.deepcopy(self.finalMatrix))
                self.result2.append(checkingList.copy())
            while True:
                resource = []
                for rowIndex in range(len(self.finalMatrix)):
                    resource.append(self.finalMatrix[rowIndex][0])
                if min(resource) < 0:
                    swapBasicVariableIndex = resource.index(min(resource))
                    swapNonBasicVariableIndex = utils.findDualSwapNonBasicVariableIndex(self.finalMatrix, swapBasicVariableIndex, self.unitIndexList, checkingList)
                    if swapNonBasicVariableIndex == -1:
                        self.resultFlag = "Unbounded Solution"
                        return
                    # Gauss transform -> new unit matrix.
                    self.finalMatrix = utils.transformToUnitMatrix(self.finalMatrix, swapNonBasicVariableIndex, swapBasicVariableIndex)
                    self.unitIndexList[swapBasicVariableIndex] = swapNonBasicVariableIndex
                    checkingList = utils.getCheckingNumber(coefficientList, self.unitIndexList, self.finalMatrix)
                    if self.stage1Flag:
                        self.result1.append(self.unitIndexList.copy())
                        self.result1.append(copy.deepcopy(self.finalMatrix))
                        self.result1.append(checkingList.copy())
                    else:
                        self.result2.append(self.unitIndexList.copy())
                        self.result2.append(copy.deepcopy(self.finalMatrix))
                        self.result2.append(checkingList.copy())
                else:
                    break
        # In the Stage 1, there is no need to judge the solution by the checkingList.
        if not self.stage1Flag:
            if max(checkingList) < 0:
                self.resultFlag = "Unique Optimal Solution"
            elif max(checkingList) > 0:
                self.resultFlag = "Unbounded Solution"
            elif max(checkingList) <= 0:
                nonBasicVariableList = []
                for variable in range(1, len(self.coefficientList)):
                    if variable not in self.unitIndexList:
                        nonBasicVariableList.append(variable)
                nonBasicVariableCheckingNumberList = []
                for nonBasicVariable in range(len(nonBasicVariableList)):
                    nonBasicVariableCheckingNumberList.append(checkingList[nonBasicVariable])
                if 0 in nonBasicVariableCheckingNumberList:
                    self.resultFlag = "Alternative Optimal Solution"