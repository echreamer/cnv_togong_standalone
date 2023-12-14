import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QSplitter, QLabel

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Horizontal Splitter Example')
window.setGeometry(100, 100, 400, 300)

vbox = QVBoxLayout()
group1 = QGroupBox('Group 1')
group2 = QGroupBox('Group 2')

# 수평 레이아웃과 라벨 추가
vbox1 = QVBoxLayout()
label1 = QLabel('Content for Group 1')
vbox1.addWidget(label1)
group1.setLayout(vbox1)

vbox2 = QVBoxLayout()
label2 = QLabel('Content for Group 2')
vbox2.addWidget(label2)
group2.setLayout(vbox2)

# 수평 스플리터 추가
splitter = QSplitter()
splitter.setOrientation(0)  # 수평 방향으로 설정
splitter.addWidget(group1)
splitter.addWidget(group2)
splitter.setSizes([150, 150])  # 각 그룹의 초기 크기 설정

vbox.addWidget(splitter)
window.setLayout(vbox)
window.show()

sys.exit(app.exec_())
