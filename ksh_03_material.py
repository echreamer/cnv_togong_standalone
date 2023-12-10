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


class ksh_03_material(QWidget):

    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()  # initUI 메서드 호출
    def initUI(self):
        
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        
        ## 레이아웃 - 왼쪽 ----------------------------------------------------------------------------------
        vbox_1 = QVBoxLayout()
        hbox.addLayout(vbox_1)
        
        ## 레이아웃 - 오른쪽 ----------------------------------------------------------------------------------
        vbox_2 = QVBoxLayout()
        hbox.addLayout(vbox_2)


        # 그룹박스 생성
        vbox_1.addWidget(self.Group1())
        vbox_1.addWidget(self.Group2())
        vbox_1.addWidget(self.Group3())
        

    #그룹박스 - 파일 불러오기 박스 ------------------------------------------------------------------ 
    def Group1(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        ## 버튼 생성 - 3
        self.btn3 = CNV_Button('굴착계획평면도 가져오기')
        vbox.addWidget(self.btn3)
        
        # 파일 경로 라벨 생성
        self.file_path_label_3 = CNV_Label("파일 경로:")
        vbox.addWidget(self.file_path_label_3)
     
        
        return groupbox
    
    #그룹박스 - 지형 --------------------------------------------------------------------------   
    def Group2(self):
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
        
        # '지형'테이블 위젯 생성--------------------
        self.topo_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.topo_table.setColumnCount(2)

        self.topo_table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.topo_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # # 두 번째 열에 콤보박스 추가 <- ksh_UI.py 파일에서 코드 생성
        # for i in range(self.table.rowCount()):
        #     combo = CNV_ComboBox()
        #     combo.addItems(["Option 1", "Option 2", "Option 3"])
        #     self.table.setCellWidget(i, 1, combo)
            
        # 행의 헤더 숨기기
        header = self.topo_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.topo_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab1 = tabs.widget(0)
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.topo_table)
        tab1.setLayout(tab1_layout)

        vbox.addWidget(tabs)

        # 버튼 생성
        self.topo_btn = CNV_Button('지형 작성')
        tab1_layout.addWidget(self.topo_btn)
          
        # '터파기'테이블 위젯 생성--------------------
        
        self.digging_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.digging_table.setColumnCount(2)

        self.digging_table.setHorizontalHeaderItem(0, QTableWidgetItem("터파기 구역"))
        self.digging_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # # 두 번째 열에 콤보박스 추가 <- ksh_UI.py 파일에서 코드 생성
        # for i in range(self.table.rowCount()):
        #     combo = CNV_ComboBox()
        #     combo.addItems(["Option 1", "Option 2", "Option 3"])
        #     self.table.setCellWidget(i, 1, combo)
            
        # 행의 헤더 숨기기
        header = self.digging_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.digging_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab2 = tabs.widget(1)
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self.digging_table)
        tab2.setLayout(tab2_layout)

        vbox.addWidget(tabs)

        # 버튼 생성
        self.digging_btn = CNV_Button('터파기 작성')
        tab2_layout.addWidget(self.digging_btn)
           
        return groupbox

    #그룹박스 - 부재 ------------------------------------------------------------------ 
    def Group3(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb2 = CNV_TitleLabel('부재')
        vbox.addWidget(lb2)
        
        # 탭 위젯 생성
        tabs = CNV_TabWidget()
        tabs.addTab(QWidget(), '파일')
        tabs.addTab(QWidget(), '흙막이')
        tabs.addTab(QWidget(), '버팀대')
        tabs.addTab(QWidget(), '복공판')
        
        # '파일'테이블 위젯 생성--------------------
        self.pile_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.pile_table.setColumnCount(2)

        self.pile_table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.pile_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # 행의 헤더 숨기기
        header = self.pile_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.pile_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab1 = tabs.widget(0)
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(self.pile_table)
        tab1.setLayout(tab1_layout)

        vbox.addWidget(tabs)        

        # '흙막이'테이블 위젯 생성--------------------
        self.mudblock_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.mudblock_table.setColumnCount(2)

        self.mudblock_table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.mudblock_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # 행의 헤더 숨기기
        header = self.mudblock_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.mudblock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab2 = tabs.widget(1)
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self.mudblock_table)
        tab2.setLayout(tab2_layout)

        vbox.addWidget(tabs)       
        
        # '버팀대'테이블 위젯 생성--------------------
        self.bracing_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.bracing_table.setColumnCount(2)

        self.bracing_table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.bracing_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # 행의 헤더 숨기기
        header = self.bracing_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.bracing_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab3 = tabs.widget(2)
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(self.bracing_table)
        tab3.setLayout(tab3_layout)

        vbox.addWidget(tabs)       
         
        # '복공판'테이블 위젯 생성--------------------
        self.board_table = CNV_TableWidget()
        # self.table.setRowCount(8)
        self.board_table.setColumnCount(2)

        self.board_table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        self.board_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))

        # 행의 헤더 숨기기
        header = self.board_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.board_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        # 탭에 테이블 추가
        tab4 = tabs.widget(3)
        tab4_layout = QVBoxLayout()
        tab4_layout.addWidget(self.board_table)
        tab4.setLayout(tab4_layout)

        vbox.addWidget(tabs)       
         
        return groupbox


if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    w = ksh_03_material()
    w.resize(600, 800)
    filename = sys.argv[1]
    if os.path.isfile(filename):
        w.load_ifc_file(filename)
        w.show()
    sys.exit(app.exec_())
