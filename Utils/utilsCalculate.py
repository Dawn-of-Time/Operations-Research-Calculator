# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

from fractions import Fraction

# Swap 2 elements in a list.
def swap(object:list, position1:int, position2:int) -> None:
    temp = object[position1]
    object[position1] = object[position2]
    object[position2] = temp

# Add one column to the matrix.
def addColumn(matrix:list, addColumn:list) -> list:
    for columnIndex in range(len(addColumn)):
        matrix[columnIndex].append(addColumn[columnIndex])
    return matrix

# Find a unit matrix, and return the index list.
def findUnitMatrix(matrix:list) -> list:
    # Construct the matrix as column vectors.
    rowNum = len(matrix)
    columnNum = len(matrix[0])
    newMatrix = []
    unitIndexList = []
    # Change the matrix from a list of row vectors to a list of column vectors.
    for columnIndex in range(columnNum):
        column = []
        for rowIndex in range(rowNum):
            column.append(matrix[rowIndex][columnIndex])
        newMatrix.append(column)
    # Find the unit vectors in turn.
    for rowIndex in range(rowNum):
        findFlag = False
        tempColumn = [0] * rowNum
        tempColumn[rowIndex] = 1
        for index in range(len(newMatrix)):
            if tempColumn == newMatrix[index]:
                unitIndexList.append(index) # Record the position of the unit vector.
                findFlag = True
        if not findFlag:
            unitIndexList.append(-1) # Can not find.
    return unitIndexList

def getCheckingNumber(value_matrix:list, unitIndexList:list, finalMatrix:list) -> list:
    checkingList = []
    for value_index in range(0, len(value_matrix)):
        value = value_matrix[value_index]
        for unit_index in range(len(unitIndexList)):
            value -= (value_matrix[unitIndexList[unit_index]] * finalMatrix[unit_index][value_index])
        checkingList.append(value)
    return checkingList

def checkout(checkingList) -> bool:
    for checking_num in checkingList[1:]:
        if checking_num > 0:
            return False
    return True

def findSwapBasicVariableIndex(finalMatrix:list, swapNonBasicVariableIndex:int, unitIndexList:list) -> int:
    ratioList = [] # All ratios.
    newRatioList = [] # A list of conforming ratios.
    for rowIndex in range(len(finalMatrix)):
        if finalMatrix[rowIndex][swapNonBasicVariableIndex] > 0:
            ratio = Fraction(finalMatrix[rowIndex][0], finalMatrix[rowIndex][swapNonBasicVariableIndex])
            ratioList.append(ratio)
            newRatioList.append(ratio)
        else:
            ratioList.append('M')
    if len(newRatioList) == 0:
        return -1
    # If there is more than one minimum, choose the one with the smallest index (changing artificial variables is preferred).
    return ratioList.index(min(newRatioList))

def findDualSwapNonBasicVariableIndex(finalMatrix:list, minResourceIndex:int, unitIndexList:list, checkingList:list) -> int:
    ratioList = [] # All ratios.
    newRatioList = [] # A list of conforming ratios.
    for columnIndex in range(len(finalMatrix[0])):
        if finalMatrix[minResourceIndex][columnIndex] < 0:
            ratio = Fraction(checkingList[columnIndex], finalMatrix[minResourceIndex][columnIndex])
            ratioList.append(ratio)
            newRatioList.append(ratio)
        else:
            ratioList.append('M')
    if len(newRatioList) == 0:
        return -1
    # If there is more than one minimum, choose the one with the smallest index.(Bland)
    return ratioList.index(min(newRatioList))

def transformToUnitMatrix(finalMatrix:list, swapNonBasicVariableIndex:int, swap_basic_variable_index:int) -> list:
    coefficient = finalMatrix[swap_basic_variable_index][swapNonBasicVariableIndex]
    for columnIndex in range(len(finalMatrix[0])):
        finalMatrix[swap_basic_variable_index][columnIndex] = Fraction(finalMatrix[swap_basic_variable_index][columnIndex], coefficient)
    for rowIndex in range(len(finalMatrix)):
        if rowIndex != swap_basic_variable_index:
            temp = finalMatrix[rowIndex][swapNonBasicVariableIndex]
            for columnIndex in range(len(finalMatrix[0])):
                finalMatrix[rowIndex][columnIndex] -= (finalMatrix[swap_basic_variable_index][columnIndex] * temp)
    return finalMatrix