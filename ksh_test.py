from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QTableWidgetItem, QTableWidget, QVBoxLayout, QWidget
import sys

def on_button_click():
    selected_items = []
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.cellWidget(row, col)  # 셀의 위젯(콤보박스) 가져오기
            if isinstance(item, QComboBox):
                selected_item = item.currentText()  # 현재 선택된 아이템 가져오기
                selected_items.append(selected_item)

    print(f"Selected items: {selected_items}")

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()

table = QTableWidget()
table.setRowCount(2)
table.setColumnCount(2)

for i in range(table.rowCount()):
    for j in range(table.columnCount()):
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        table.setCellWidget(i, j, combo)

button = QPushButton("Extract Selected Items")
button.clicked.connect(on_button_click)

layout.addWidget(table)
layout.addWidget(button)
window.setLayout(layout)
window.show()

sys.exit(app.exec_())
