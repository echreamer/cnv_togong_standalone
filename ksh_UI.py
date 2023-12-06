# import time
import os.path
from IFCCustomDelegate import *

from ksh_layer_selection import *
from ksh_report_result import *
from ksh_height_setting import *
from ksh_information import *

from IFCListingWidget import *
import cnv_methods as cnv

from os import environ

import ezdxf

from ksh_style import *
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

from IFCCustomDelegate import *
from ksh_style import *

from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QVBoxLayout, QWidget
##_사용함수





######


class MainWindow(QMainWindow):

    #해상도별 글자크기 강제 고정
    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"


    def __init__(self):
        super().__init__()

        # 전역변수 설정
        self.dxf_1 = None #현황도 dxf파일
        self.dxf_1_layers = None #현황도 dxf파일의 레이어 리스트



        self.setStyleSheet("background-color: #ffffff;")        
        
        # 위젯 생성-------------------------------------------------------------------------------------
        
        
        self.view_layer_selection = ksh_layer_selection() #레이어 지정
        self.view_layer_selection.setMinimumWidth(350)

        self.ksh_report_result = ksh_report_result() #보링점
        self.ksh_report_result.setMinimumWidth(350)

        self.ksh_height_setting = ksh_height_setting() #높이 설정
        self.ksh_height_setting.setMinimumWidth(350)

        self.ksh_information = ksh_information() #부재 정보 입력
        self.ksh_information.setMinimumWidth(350)

        # 위젯 배치------------------------------------------------------------------------------------

        self.dock2 = CNV_DockWidget('레이어 선택', self)
        self.dock2.setWidget(self.view_layer_selection)
        self.dock2.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock2)

        self.dock3 = CNV_DockWidget('시추조사 결과 입력', self)
        self.dock3.setWidget(self.ksh_report_result)
        self.dock3.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock3)

        self.dock4 = CNV_DockWidget('높이 설정', self)
        self.dock4.setWidget(self.ksh_height_setting)
        self.dock4.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock4)

        self.dock5 = CNV_DockWidget('부재 정보 입력', self)
        self.dock5.setWidget(self.ksh_information)
        self.dock5.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock5)
        
        
        #dxf파일 열기 액션


        self.view_layer_selection.btn.clicked.connect(self.action_dxf_open_click)


        #지형작성 액션
        self.view_layer_selection.add_btn.clicked.connect(self.action_generate_topo)




        # 프로젝트 저장 탭(툴바 생성) -------------------------------------------------------------------------------
        self.setUnifiedTitleAndToolBarOnMac(True)
        toolbar = CNV_ToolBar("My main toolbar")
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 메뉴바
        #menu_bar = self.menuBar()
        #file_menu = QMenu("&File", self)
        #menu_bar.addMenu(file_menu)

        # 프로젝트 내보내기 --------------------------------------------------------------------------
        action_save = QAction("프로젝트 내보내기", self)
        action_save.triggered.connect(self.action_save_click)
        toolbar.addAction(action_save)        
        
        
        # 체크박스(위젯가시성) -----------------------------------------------------------------------
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        spacer_widget.setStyleSheet("background-color: #EAF1FD;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 2
        self.check_2 = CNV_CheckBox("레이어 선택")
        self.check_2.stateChanged.connect(self.toggle_2)
        self.check_2.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_2)
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        spacer_widget.setStyleSheet("background-color: #EAF1FD; margin-bottom: 10px;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 3
        self.check_3 = CNV_CheckBox("시추조사 결과 입력")
        self.check_3.stateChanged.connect(self.toggle_3)
        self.check_3.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_3)
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        
        spacer_widget.setStyleSheet("background-color: #EAF1FD; margin-bottom: 10px;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 4
        self.check_4 = CNV_CheckBox("높이 설정")
        self.check_4.stateChanged.connect(self.toggle_4)
        self.check_4.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_4)
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        spacer_widget.setStyleSheet("background-color: #EAF1FD; margin-bottom: 10px;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 5
        self.check_5 = CNV_CheckBox("부재 정보 입력")
        self.check_5.stateChanged.connect(self.toggle_5)
        self.check_5.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_5)
        
        
        #메뉴바
        #file_menu.addAction(action_save)        
        
    # dxf파일 불러오기 버튼들 눌렀을 때 실행되는 함수
    def action_dxf_open_click(self):

        self.filenames, self.filter_string = QFileDialog.getOpenFileNames(self, caption="Open DXF File",
                                                                filter="DXF files (*.dxf)")

        for file in self.filenames:
            if os.path.isfile(file):
                try:
                    self.load_dxf_file(file)
                except:
                    pass


    #-----------------------------------------------------------
    # dxf파일을 로드하는 함수
    def load_dxf_file(self, filename):
        doc = ezdxf.readfile(filename)
        self.dxf_1 = doc
        self.dxf_1_layers=self.load_dxf_layers(doc)
        self.input_dxf_layer_topo_widget(self.dxf_1_layers)#콤보박스에 리스트업

        print(doc)
        print(self.dxf_1_layers)

        return doc

    #---------------------------------------------------------------
    # dxf 파일의 레이어 리스트 추출 메소드

    def load_dxf_layers(self, doc):

        try:

            layers = [layer.dxf.name for layer in doc.layers]

            return layers

        except IOError:

            print(f"Cannot open file")

            return []

        except ezdxf.DXFStructureError:

            print(f"Invalid or corrupted DXF file")

            return []
    #---------------------------------------------------------------

    # 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_topo_widget(self,layerList):
        print(layerList)
        rowCount = 2
        self.view_layer_selection.table.setRowCount(rowCount)
        self.view_layer_selection.table.setItem(0,0, QTableWidgetItem("지형 레벨 포인트"))
        self.view_layer_selection.table.setItem(1,0, QTableWidgetItem("대지경계선"))

        for i in range(self.view_layer_selection.table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_layer_selection.table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_layer_selection.table.rowCount()):
            item = self.view_layer_selection.table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)


    # ---dd
    # 지형 작성 액션 메소드
    def action_generate_topo(self):
        
        # 현재 선택된 레벨포인트용 레이어
        current_level_layer = self.view_layer_selection.table.cellWidget(0,1).currentText()
        # current_level_layer의 이름을 가진 dxf파일 내의 레이어의 좌표를 가져오고 그것을 담을 리스트에 저장
        # 리스트에 저장할 때 현재 담겨있는 리스트의 값을 확인해서 만약 동일한 값이 있다면 패스 
        # 만약 텍스트 값이 필요할 경우 동시에 그 레이어의 객체와 가장 가까운 텍스트의 값을 가져오는데 위에서 패스일 경우는 제외
        #

        

    #--------












    # 체크박스 상태 변화 함수 정의--------------------------------------------------------------
            
    def toggle_2(self, state):
        # 체크박스 상태에 따라 view_3d_quantity 위젯의 가시성을 설정
        self.dock2.setVisible(state == Qt.Checked)        
    
    def toggle_3(self, state):
        # 체크박스 상태에 따라 view_3d_quantity 위젯의 가시성을 설정
        self.dock3.setVisible(state == Qt.Checked)        
    
    def toggle_4(self, state):
        # 체크박스 상태에 따라 view_3d_quantity 위젯의 가시성을 설정
        self.dock4.setVisible(state == Qt.Checked)        
    
    def toggle_5(self, state):
        # 체크박스 상태에 따라 view_3d_quantity 위젯의 가시성을 설정
        self.dock5.setVisible(state == Qt.Checked)        

        
        
    # 프로젝트 저장 이벤트-------------------------------------------------------------------------------
    
    def action_save_click(self):
        print(self.project_folder_path + "constr_item_list.json")
        cnv.save_json(self.constr_item_list, self.project_folder_path + "constr_item_list.json")
        cnv.save_json(self.obj_constr_connect_list, self.project_folder_path + "obj_constr_connect_list.json")
        cnv.save_json(self.obj_constr_quantity_list, self.project_folder_path + "obj_constr_quantity_list.json")
    

        








def main():
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)
    app.setApplicationDisplayName("BIM Estimator")
    app.setOrganizationName("CNV")
    app.setOrganizationDomain("cnvarchiplan.com")
    app.setApplicationName("BIM Estimator")

    w = MainWindow()
    w.setWindowTitle("BIM Estimator")
    # w.resize(1920, 1080)
    filename = sys.argv[1] if len(sys.argv) >= 2 else ''
    if os.path.isfile(filename):
        w.load_ifc_file(filename)
        w.setWindowTitle(w.windowTitle() + " - " + os.path.basename(filename))
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    MainWindow.suppress_qt_warnings()
    main()