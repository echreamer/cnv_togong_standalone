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


class ksh_01_topo(QWidget):

    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()  # initUI 메서드 호출
        
        self.vbox = QVBoxLayout() 
        
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
       
        # 버튼 생성
        self.topo_btn = CNV_Button('현황 지형 작성')
        vbox.addWidget(self.topo_btn)
        
        vbox.addWidget(self.Group3())
        
        # 버튼 생성
        self.stratum_btn = CNV_Button('지층 생성')
        self.stratum_btn.clicked.connect(self.addBoringPoint)        
        vbox.addWidget(self.stratum_btn)
        
        
    #그룹박스 - 파일 불러오기 박스 ------------------------------------------------------------------ 
    def Group1(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정

        ## 버튼 생성 - 1
        self.btn1 = CNV_Button('현황측량도 가져오기')
        vbox.addWidget(self.btn1)
        
        # 파일 경로 라벨 생성
        self.file_path_label_1 = CNV_Label("파일 경로:")
        vbox.addWidget(self.file_path_label_1)
        
        return groupbox
    
    #그룹박스 - 지형 --------------------------------------------------------------------------   
    def Group2(self):
        groupbox = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)  # 그룹박스에 레이아웃 설정
        
        # '지형'테이블 위젯 생성--------------------
        self.topo_table = CNV_TableWidget()
        self.topo_table.setColumnCount(2)
        self.topo_table.setHorizontalHeaderItem(0, QTableWidgetItem("구분_"))
        self.topo_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택_"))
            
        # 행의 헤더 숨기기
        header = self.topo_table.verticalHeader()
        header.hide()       

        # 테이블 열 너비 조정
        self.topo_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        vbox.addWidget(self.topo_table)

        return groupbox

    #그룹박스 - 보링점 ------------------------------------------------------------------ ----
    def Group3(self):
        groupbox3 = CNV_GroupBox()
        
        vbox = QVBoxLayout()
        groupbox3.setLayout(vbox)  # 그룹박스에 레이아웃 설정

        # 버튼 생성
        self.boring_point_add_btn = CNV_Button('보링점 추가')
        self.boring_point_add_btn.clicked.connect(self.addBoringPoint)        
        vbox.addWidget(self.boring_point_add_btn)
        
        # 탭뷰 생성
        self.tabs = CNV_TabWidget()
        vbox.addWidget(self.tabs)
        
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        
        # 체크박스(지층레벨 예측을 위한 알고리즘 선택)
        self.check_line = CNV_CheckBox("선형보간")
        self.check_line.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox.addWidget(self.check_line)
        
        self.check_spline = CNV_CheckBox("스플라인보간")
        self.check_spline.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox.addWidget(self.check_spline)
        
        self.check_k = CNV_CheckBox("K-최근점이웃(KNN)")
        self.check_k.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox.addWidget(self.check_k)
        
        return groupbox3
   
    #새로운 보링점 추가 --------------------------------------
    
    
    def addBoringPoint(self):
        new_tab = QWidget()  # 새로운 탭 생성
        self.tabs.addTab(new_tab, f'NX-{self.tabs.count() + 1}')  # 탭 추가 및 이름 설정
        
        if self.tabs.count() > 1:  # 첫 번째 탭 이후에만 버튼 추가
            index = self.tabs.count() - 1  # 새로운 탭의 인덱스
            self.addCloseButton(index)                 

        # 탭에 위젯 배치
        tab_layout = QVBoxLayout(new_tab)
        
        # 보링점 정보 입력칸
        hbox = QHBoxLayout()
        tab_layout.addLayout(hbox)  # 수평 레이아웃을 수직 레이아웃에 추가

        name_lb = CNV_Label('이름 : ')
        hbox.addWidget(name_lb)

        name_input = QLineEdit()
        hbox.addWidget(name_input)
        
        x_lb = CNV_Label('X : ')
        hbox.addWidget(x_lb)

        x_input = QLineEdit()
        hbox.addWidget(x_input)

        y_lb = CNV_Label('Y : ')
        hbox.addWidget(y_lb)

        y_input = QLineEdit()
        hbox.addWidget(y_input)

        z_lb = CNV_Label('Z : ')
        hbox.addWidget(z_lb)

        z_input = QLineEdit()
        hbox.addWidget(z_input)
        
        
        
        
        
        NX_table = CNV_TableWidget()
        NX_table.setRowCount(8)
        NX_table.setColumnCount(2)
        NX_table.setHorizontalHeaderItem(0, QTableWidgetItem("지층"))
        NX_table.setHorizontalHeaderItem(1, QTableWidgetItem("층후(M)"))



        # 각 행에 콤보박스 추가
        for i in range(NX_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(["매립층", "퇴적층(실트)", "퇴적층(모래)", "퇴적층(자갈)", "풍화토", "풍화암", "보통암", "경암"])
            NX_table.setCellWidget(i, 0, combo)

        header = NX_table.verticalHeader()
        header.hide()
        NX_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        tab_layout.addWidget(NX_table)    
        
    def addCloseButton(self, index):
        # 탭의 index에 해당하는 위치에 닫기 버튼 추가
        close_btn = CNV_CloseButton('X')
        close_btn.clicked.connect(lambda _, idx=index: self.closeTab(idx))  # 클릭 시 탭 닫기
        self.tabs.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)  # 오른쪽에 버튼 추가

    def closeTab(self, index):
        if index != -1:
            self.tabs.removeTab(index)  # 선택한 탭 닫기

            # 삭제된 탭 이후의 탭들에 대해 닫기 버튼 재설정
            for i in range(self.tabs.count()):
                self.addCloseButton(i)

if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    w = ksh_01_topo()
    w.resize(600, 800)
    filename = sys.argv[1]
    if os.path.isfile(filename):
        w.load_ifc_file(filename)
        w.show()
    sys.exit(app.exec_())