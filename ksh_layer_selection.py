import sys
import os.path
import cnv_methods as cnv
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except Exception:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

import ifcopenshell
from IFCCustomDelegate import *
from ksh_style import *


class ksh_layer_selection(QWidget):

    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()  # initUI 메서드 호출
    def initUI(self):
        
       
        # 기본 폰트
        #self.font = QFont()
        #self.font.setBold(False)       # 굵게 설정            
        #self.font.setFamily('맑은고딕')  # 원하는 폰트 패밀리로 변경
        #self.font.setPointSize(int(self.width() / 70))  # 20은 크기 조절을 위한 임의의 비율 상수

        # 수직 박스 레이아웃 생성
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        # 공간 확보
        spacer = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        vbox.addSpacerItem(spacer)   

        # 버튼 생성
        self.btn = CNV_Button('파일 불러오기')
        vbox.addWidget(self.btn)
        self.show()    

        # 그룹박스 생성
        vbox.addWidget(self.Group1())
        vbox.addWidget(self.Group2())

    
    #그룹박스 - 지형 --------------------------------------------------------------------------   
    def Group1(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('지형')
        vbox.addWidget(lb1)        

        # 탭 위젯 생성
        tabs = CNV_TabWidget()
        tabs.addTab(QWidget(), '현황')
        tabs.addTab(QWidget(), '터파기')  # 빈 탭 추가
        
        # 테이블 위젯 생성
<<<<<<< HEAD
        self.table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.table.setColumnCount(2)
=======
        table = CNV_TableWidget()
        table.setRowCount(2)
        table.setColumnCount(2)
>>>>>>> a89c00a9c0579b94fb65d8dffc7f4b6ec86c0258

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

<<<<<<< HEAD
        # # 두 번째 열에 콤보박스 추가 <- ksh_UI.py 파일에서 코드 생성
        # for i in range(self.table.rowCount()):
        #     combo = CNV_ComboBox()
        #     combo.addItems(["Option 1", "Option 2", "Option 3"])
        #     self.table.setCellWidget(i, 1, combo)
=======
        # 고정값으로 첫 번째 열의 텍스트 설정
        table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))
        
        # 첫 번째 열에 콤보박스 추가
        for i in range(table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(["Option 1", "Option 2", "Option 3"])
            table.setCellWidget(i, 1, combo)
>>>>>>> a89c00a9c0579b94fb65d8dffc7f4b6ec86c0258
            
        # 행의 헤더 숨기기
        header = self.table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab1 = tabs.widget(0)
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.table)
        tab1.setLayout(tab1_layout)

        vbox.addWidget(tabs)

        # 버튼 생성
        add_btn = CNV_Button('지형 작성')
        tab1_layout.addWidget(add_btn)
           
        return groupbox
    
    #그룹박스 - 부재 ------------------------------------------------------------------ 
    def Group2(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb2 = CNV_TitleLabel('부재')
        vbox.addWidget(lb2)
        
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        tabs = CNV_TabWidget()
        tabs.addTab(tab1, '파일')
        tabs.addTab(tab2, '흙막이')
        tabs.addTab(tab3, '버팀대')
        tabs.addTab(tab4, '복공판')
        
        # 테이블 위젯 생성
        table = CNV_TableWidget()
        table.setRowCount(8)
        table.setColumnCount(2)

        table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # 첫 번째 열에 콤보박스 추가
        for i in range(table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(["Option 1", "Option 2", "Option 3"])
            table.setCellWidget(i, 1, combo)
            
        # 행의 헤더 숨기기
        header = table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab1 = tabs.widget(0)
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(table)
        tab1.setLayout(tab1_layout)
        
        vbox.addWidget(tabs)

        

        return groupbox



if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    w = ksh_layer_selection()
    w.resize(600, 800)
    filename = sys.argv[1]
    if os.path.isfile(filename):
        w.load_ifc_file(filename)
        w.show()
    sys.exit(app.exec_())
