# Copyright (c) 2023 Dawn
# Operations Research Calculator is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2. 
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2 
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.  

from PyQt6.QtCore import Qt
import PyQt6.QtWidgets as QtWidgets
class MatrixTable(QtWidgets.QTableWidget):
    def __init__(self, rows: int, columns: int, parent):
        super().__init__(rows, columns, parent)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectItems)
        self.itemSelectionChanged.connect(self.on_item_selection_changed)

    def on_item_selection_changed(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            item.setBackground(Qt.GlobalColor.lightGray)

        # 清除未选中单元格的背景颜色
        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                cell = self.item(r, c)
                if cell and cell not in selected_items:
                    cell.setBackground(Qt.GlobalColor.white)

    # def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
    #     index = self.selection_model.selectedIndexes()
    #     if len(index) != 0:
    #         print(index)
    #         x = index[0].row()
    #         y = index[0].column()
    #         for rowIndex in range(self.rowCount()):
    #             self.itemAt(rowIndex, y).setBackground(QColor(135, 206, 250))
    #         for columnIndex in range(self.columnCount()):
    #             self.itemAt(x, columnIndex).setBackground(QColor(135, 206, 250))
    #     else:
    #         super().selectionChanged(selected, deselected)