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


class ksh_02_digging(QWidget):

    
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


        # 그룹박스 생성
        vbox.addWidget(self.Group1())
        vbox.addWidget(self.Group2())
        vbox.addWidget(self.Group3())

        # 버튼 생성
        self.digging_btn = CNV_Button('터파기 작성')
        vbox.addWidget(self.digging_btn)
        

    #그룹박스 - 파일 불러오기 박스 ------------------------------------------------------------------ 
    def Group1(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        ## 버튼 생성 - 2
        self.digging_file_import_btn = CNV_Button('터파기파일 가져오기')
        vbox.addWidget(self.digging_file_import_btn)
        
        # 파일 경로 라벨 생성
        self.file_path_label_2 = CNV_Label("파일 경로:")
        vbox.addWidget(self.file_path_label_2)
     
        
        return groupbox
    
    #그룹박스 - 지형 --------------------------------------------------------------------------   
    def Group2(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정

        self.digging_table = CNV_TableWidget()
        self.digging_table.setColumnCount(2)

        self.digging_table.setHorizontalHeaderItem(0, QTableWidgetItem("구분"))
        self.digging_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))
            
        # 행의 헤더 숨기기
        header = self.digging_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.digging_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        
        vbox.addWidget(self.digging_table)
           
        return groupbox

    #그룹박스 - 부재 ------------------------------------------------------------------ 
    def Group3(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)
        
        # 라벨 생성
        lb1 = CNV_TitleLabel('터파기 높이 설정')
        vbox.addWidget(lb1)
        
        # 테이블 위젯 생성
        table2 = CNV_TableWidget()
        table2.setRowCount(10)
        table2.setColumnCount(2)
        

        table2.setHorizontalHeaderItem(0, QTableWidgetItem("레이어"))
        table2.setHorizontalHeaderItem(1, QTableWidgetItem("mm"))

        # 첫 번째 열에 콤보박스 추가
        for i in range(table2.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(["layer 1", "layer 2", "layer 3"])
            table2.setCellWidget(i, 0, combo)


        # 행의 헤더 숨기기
        header = table2.verticalHeader()
        header.hide()       
        
        # 테이블 열 너비 조정
        table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
               
        vbox.addWidget(table2)

        
        return groupbox



if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    w = ksh_02_digging()
    w.resize(600, 800)
    filename = sys.argv[1]
    if os.path.isfile(filename):
        w.load_ifc_file(filename)
        w.show()
    sys.exit(app.exec_())
