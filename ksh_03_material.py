import sys
import os.path
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except Exception:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

import ifcopenshell
from ksh_style import *


class ksh_03_material(QWidget):

    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()  # initUI 메서드 호출
    def initUI(self):

        vbox_1 = QVBoxLayout()
        self.setLayout(vbox_1)

        group = CNV_Simple_GroupBox()
        vbox_1.addWidget(group)
        
        vbox_2 = QVBoxLayout()
        group.setLayout(vbox_2)

        hbox = QHBoxLayout()
        vbox_2.addLayout(hbox)
       
        # 버튼 생성
        self.material_btn = CNV_Button('부재 작성')
        vbox_2.addWidget(self.material_btn)
        
        
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
        
        vbox_2.addWidget(self.Group4())
        vbox_2.addWidget(self.Group5())
        vbox_2.addWidget(self.Group6())
        
    #그룹박스 - 파일 불러오기 박스 ------------------------------------------------------------------ 
    
    def Group1(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        ## 버튼 생성 - 3
        self.material_file_import_btn = CNV_Button('굴착계획평면도 가져오기')
        vbox.addWidget(self.material_file_import_btn)
        
        # 파일 경로 라벨 생성
        self.file_path_label_3 = CNV_Label("파일 경로:")
        self.file_path_label_3.setWordWrap(True)
        vbox.addWidget(self.file_path_label_3)
     
        
        return groupbox
    
    #그룹박스 - 지형 --------------------------------------------------------------------------   
    def Group2(self):
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

    #그룹박스 - 부재 ------------------------------------------------------------------ 
    def Group3(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('스트러트 높이 설정')
        vbox.addWidget(lb1)
        
        # 테이블 위젯 생성
        table1 = CNV_TableWidget()
        table1.setRowCount(3)
        table1.setColumnCount(2)
        
        table1.setHorizontalHeaderItem(0, QTableWidgetItem())
        table1.setHorizontalHeaderItem(1, QTableWidgetItem("mm"))
            
        # 행의 헤더 숨기기
        header = table1.verticalHeader()
        header.hide()       
        
        # 테이블 열 너비 조정
        table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        vbox.addWidget(table1)
        
        # 버튼들을 담을 위젯 생성
        button_widget = QWidget()  
        button_widget.setStyleSheet("background-color: #EAF1FD; font-size:15;")
        button_layout = QHBoxLayout()
        
        # 버튼 생성
        add_btn = CNV_Button('행 추가')
        add_btn.clicked.connect(self.addRow)
        button_layout.addWidget(add_btn)
        
        delete_btn = CNV_Button('행 삭제')
        delete_btn.clicked.connect(self.deleteRow) 
        button_layout.addWidget(delete_btn)
        
        # 버튼 레이아웃을 위젯에 설정
        button_widget.setLayout(button_layout)  
        vbox.addWidget(button_widget)
        
        # 열 너비 설정
        table1.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table1.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table1.setColumnWidth(2, 10)  # 세 번째 열의 너비를 100으로 설정 (조절 가능)
        
        self.group3_box = groupbox        
        
        return groupbox
    
    
    # '추가' 버튼 클릭 시 호출되는 메서드
    def addRow(self):
        
        table1 = self.group3_box.findChild(QTableWidget)
        if table1 is not None:
            currentRowCount = table1.rowCount()
            table1.setRowCount(currentRowCount + 1)

    def deleteRow(self, row):
        table1 = self.group3_box.findChild(QTableWidget)
        if table1 is not None:
            table1.removeRow(row)    

    
    #그룹박스 - 부재 ------------------------------------------------------------------ 
    def Group4(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('파일')
        vbox.addWidget(lb1)
        
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        tabs = CNV_TabWidget()
        tabs.addTab(tab1, 'PRD')
        tabs.addTab(tab2, 'RCD')
        tabs.addTab(tab3, 'PHC')
        
        # 테이블 위젯 생성
        table = CNV_TableWidget()
        table.setRowCount(8)
        table.setColumnCount(2)

        table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("사이즈"))

            
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

    
    #그룹박스 - 흙막이 ------------------------------------------------------------------ 
    def Group5(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('흙막이')
        vbox.addWidget(lb1)
        
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        tabs = CNV_TabWidget()
        tabs.addTab(tab1, 'CIP')
        tabs.addTab(tab2, 'PILE')
        tabs.addTab(tab3, 'H-PILE')
        tabs.addTab(tab4, '슬러리월')
        
        # 테이블 위젯 생성
        table = CNV_TableWidget()
        table.setRowCount(8)
        table.setColumnCount(2)

        table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("사이즈"))

            
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
    

    #그룹박스 - 버팀대 ------------------------------------------------------------------ 
    def Group6(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('버팀대')
        vbox.addWidget(lb1)
        
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        tabs = CNV_TabWidget()
        tabs.addTab(tab1, '센터파일')
        tabs.addTab(tab2, '어스앵커')
        tabs.addTab(tab3, '스트러트')
        tabs.addTab(tab4, '띠장')
        
        # 테이블 위젯 생성
        table = CNV_TableWidget()
        table.setRowCount(8)
        table.setColumnCount(2)

        table.setHorizontalHeaderItem(0, QTableWidgetItem("부재"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("사이즈"))

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
    
