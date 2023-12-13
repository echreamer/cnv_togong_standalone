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


class ksh_01_topo(QWidget):

    
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()  # initUI 메서드 호출
        self.vbox = QVBoxLayout() 
        self.undo_stack = []
        self.redo_stack = []
        self.current_tab = None
        
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
        self.topo_file_import_btn = CNV_Button('현황측량도 가져오기')
        vbox.addWidget(self.topo_file_import_btn)
        
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
        self.topo_table.setHorizontalHeaderItem(0, QTableWidgetItem("구분"))
        self.topo_table.setHorizontalHeaderItem(1, QTableWidgetItem("레이어선택"))
            
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

        hbox1 = QHBoxLayout()
        vbox.addLayout(hbox1)

        # 버튼 생성SS
        self.boring_point_add_btn = CNV_Button('보링점 추가')
        self.boring_point_add_btn.clicked.connect(lambda: self.addBoringPoint("","","",""))        
        hbox1.addWidget(self.boring_point_add_btn)
        
        self.boring_point_delete_btn = CNV_Button('보링점 삭제')
        self.boring_point_delete_btn.clicked.connect(lambda: self.deleteBoringPoint("","","",""))        
        hbox1.addWidget(self.boring_point_add_btn)
        
        # 탭뷰 생성
        self.tabs = CNV_TabWidget()
        vbox.addWidget(self.tabs)
        
        hbox2 = QHBoxLayout()
        vbox.addLayout(hbox2)
        
        # 체크박스(지층레벨 예측을 위한 알고리즘 선택)
        self.check_line = CNV_CheckBox("선형보간")
        self.check_line.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox2.addWidget(self.check_line)
        
        self.check_spline = CNV_CheckBox("스플라인보간")
        self.check_spline.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox2.addWidget(self.check_spline)
        
        self.check_k = CNV_CheckBox("K-최근점이웃(KNN)")
        self.check_k.setChecked(False)  # 체크박스 초기에 선택안된 상태로 설정
        hbox2.addWidget(self.check_k)
        
        return groupbox3
   
    #새로운 보링점 추가 --------------------------------------
    
    
    def addBoringPoint(self,name,x,y,z):
        new_tab = QWidget()  # 새로운 탭 생성
        self.tabs.addTab(new_tab, f'{self.tabs.count() + 1}')  # 탭 추가 및 이름 설정
        self.current_tab = new_tab
        
        # 탭에 위젯 배치
        tab_layout = QVBoxLayout(new_tab)
        
        # 보링점 정보 입력칸
        hbox = QHBoxLayout()
        tab_layout.addLayout(hbox)  # 수평 레이아웃을 수직 레이아웃에 추가

        name_lb = CNV_Label('이름 : ')
        hbox.addWidget(name_lb)
        
        name_input = QLineEdit()
        hbox.addWidget(name_input)
        name_input.setText(name)

        x_lb = CNV_Label('X : ')
        hbox.addWidget(x_lb)

        x_input = QLineEdit()
        hbox.addWidget(x_input)
        x_input.setText(x)

        y_lb = CNV_Label('Y : ')
        hbox.addWidget(y_lb)

        y_input = QLineEdit()
        hbox.addWidget(y_input)
        y_input.setText(y)

        z_lb = CNV_Label('Z : ')
        hbox.addWidget(z_lb)

        z_input = QLineEdit()
        hbox.addWidget(z_input)
        z_input.setText(z)
        
        
        # 테이블 배치
        NX_table = CNV_TableWidget()
        NX_table.setRowCount(0)
        NX_table.setColumnCount(2)
        NX_table.setHorizontalHeaderItem(0, QTableWidgetItem("지층"))
        NX_table.setHorizontalHeaderItem(1, QTableWidgetItem("층후(M)"))

        header = NX_table.verticalHeader()
        header.hide()
        NX_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tab_layout.addWidget(NX_table)    

        hbox_2 = QHBoxLayout()
        tab_layout.addLayout(hbox_2)

        # 테이블 행 추가 버튼 추가
        self.row_add_btn = CNV_Button('행 추가')
        self.row_add_btn.clicked.connect(self.addRow)
        hbox_2.addWidget(self.row_add_btn)

        # 테이블 행 추가 버튼 추가
        self.row_delete_btn = CNV_Button('행 삭제')
        self.row_delete_btn.clicked.connect(self.deleteRow)
        hbox_2.addWidget(self.row_delete_btn)
            
    def addRow(self):
        current_tab_index = self.tabs.currentIndex()
        self.current_tab = self.tabs.widget(current_tab_index)
        if self.current_tab:
            # 현재 탭에서 NX_table 찾기
            nx_table = self.current_tab.findChild(CNV_TableWidget)
            if nx_table:
                currentRowCount = nx_table.rowCount()
                nx_table.setRowCount(currentRowCount + 1)
                
                # 새로운 행에 콤보박스 추가
                combo = CNV_ComboBox()
                combo.addItems(["매립층", "퇴적층(실트)", "퇴적층(모래)", "퇴적층(자갈)", "풍화토", "풍화암", "보통암", "경암"])
                nx_table.setCellWidget(currentRowCount, 0, combo)
                
        # 수행된 동작을 스택에 저장
        self.undo_stack.append(('add', self.current_tab, currentRowCount, self.saveComboData(self.current_tab, currentRowCount), self.saveComboCurrentIndex(self.current_tab, currentRowCount)))
        # 추가된 데이터를 임시 저장하는 스택
        self.redo_stack.clear()
        
    def deleteRow(self):
        current_tab_index = self.tabs.currentIndex()
        self.current_tab = self.tabs.widget(current_tab_index)
        if self.current_tab:
            nx_table = self.current_tab.findChild(CNV_TableWidget)
            if nx_table:
                selected_row = nx_table.currentRow()
                if selected_row >= 0:
                    # 저장할 데이터 가져오기
                    combo_data = self.saveComboData(self.current_tab, selected_row)
                    combo_current_index = self.saveComboCurrentIndex(self.current_tab, selected_row)
                    
                    # 삭제된 데이터 및 콤보박스 정보를 스택에 저장
                    self.undo_stack.append(('delete', self.current_tab, selected_row, combo_data, combo_current_index))
                    
                    # 행 삭제
                    nx_table.removeRow(selected_row)
                    
                    # 삭제된 데이터를 임시 저장하는 스택은 비워두기
                    self.redo_stack.clear()


    def undoLastAction(self):
        if self.undo_stack:
            action, tab, data, combo_data, combo_current_index = self.undo_stack.pop()  # 가장 최근 동작을 팝하여 실행 취소

            if action == 'add':
                tab.findChild(CNV_TableWidget).removeRow(data)  # 'add' 동작 실행 취소
            elif action == 'delete':
                # 'delete' 동작 실행 취소
                tab.findChild(CNV_TableWidget).insertRow(data)
                # 삭제된 데이터 복원 (콤보박스 추가 및 선택된 항목 복원)
                combo = CNV_ComboBox()
                combo.addItems(["매립층", "퇴적층(실트)", "퇴적층(모래)", "퇴적층(자갈)", "풍화토", "풍화암", "보통암", "경암"])
                tab.findChild(CNV_TableWidget).setCellWidget(data, 0, combo)
                combo.setCurrentIndex(combo_data)
                if combo_current_index is not None:  # 선택된 인덱스가 존재할 때만 설정
                    combo.setCurrentIndex(combo_current_index)

    def saveComboData(self, tab, row):
        if tab:
            nx_table = tab.findChild(CNV_TableWidget)
            if nx_table:
                combo = nx_table.cellWidget(row, 0)
                if combo:
                    return combo.currentIndex()
        return 0  # 기본값은 0으로 설정하거나 필요에 따라 다른 값을 반환하도록 설정 가능

    def saveComboCurrentIndex(self, tab, row):
        if tab:
            nx_table = tab.findChild(CNV_TableWidget)
            if nx_table:
                combo = nx_table.cellWidget(row, 0)
                if combo:
                    return combo.currentIndex()
        return None 

    # 'Ctrl + Z'를 눌렀을 때 undoLastAction() 메서드를 실행하도록 설정
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undoLastAction()
        else:
            super().keyPressEvent(event)                

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