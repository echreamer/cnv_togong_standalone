# import time
import os.path
from IFCCustomDelegate import *

from ksh_01_topo import *
from ksh_02_digging import *
from ksh_03_material import *

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

import json
import socket
import math
##_사용함수





#########

## 특정 좌표점과 가장 가까운 텍스트의 값 추출 함수
def find_nearest_text(msp, target_x, target_y):
    
    # 가장 가까운 텍스트와 거리를 저장할 변수 초기화
    nearest_text = None
    min_distance = float('inf')

    # 모든 텍스트 개체 순회
    for text in msp.query('TEXT'):
        text_x, text_y, _ = text.dxf.insert
        # 거리 계산
        distance = math.sqrt((text_x - target_x) ** 2 + (text_y - target_y) ** 2)

        # 가장 짧은 거리 업데이트
        if distance < min_distance:
            min_distance = distance
            nearest_text = text.dxf.text

    return nearest_text

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
        self.dxf_1 = None #현황측량도 dxf파일
        self.dxf_1_layers = None 
        self.dxf_2 = None #터파기 dxf파일
        self.dxf_2_layers = None 
        self.dxf_3 = None #굴착계획평면도 dxf파일
        self.dxf_3_layers = None 

        self.setStyleSheet("background-color: #ffffff;")        
        
        # 위젯 생성--------------------------------------------------------------------------------------test
        
        
        self.view_ksh_01_topo = ksh_01_topo() #레이어 지정
        self.view_ksh_01_topo.setMinimumWidth(300)

        self.view_ksh_02_digging = ksh_02_digging() #보링점
        self.view_ksh_02_digging.setMinimumWidth(300)

        self.view_ksh_03_material = ksh_03_material() #높이 설정
        self.view_ksh_03_material.setMinimumWidth(600)


        # 위젯 배치------------------------------------------------------------------------------------

        self.dock2 = CNV_DockWidget('지형', self)
        self.dock2.setWidget(self.view_ksh_01_topo)
        self.dock2.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock2)

        self.dock3 = CNV_DockWidget('터파기', self)
        self.dock3.setWidget(self.view_ksh_02_digging)
        self.dock3.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock3)

        self.dock4 = CNV_DockWidget('부재', self)
        self.dock4.setWidget(self.view_ksh_03_material)
        self.dock4.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock4)
        
        #dxf파일 열기 액션


        self.view_ksh_01_topo.btn1.clicked.connect(self.action_dxf_open_click_1)
        self.view_ksh_02_digging.btn2.clicked.connect(self.action_dxf_open_click_2)
        self.view_ksh_03_material.btn3.clicked.connect(self.action_dxf_open_click_3)
        
        
        #지형작성 액션
        self.view_ksh_01_topo.topo_btn.clicked.connect(self.action_generate_topo)




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
        self.check_2 = CNV_CheckBox("지형")
        self.check_2.stateChanged.connect(self.toggle_2)
        self.check_2.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_2)
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        spacer_widget.setStyleSheet("background-color: #EAF1FD; margin-bottom: 10px;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 3
        self.check_3 = CNV_CheckBox("터파기")
        self.check_3.stateChanged.connect(self.toggle_3)
        self.check_3.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_3)
        
        # 공간 확보
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # 너비 조절을 통해 간격 조정
        
        spacer_widget.setStyleSheet("background-color: #EAF1FD; margin-bottom: 10px;")      
        toolbar.addWidget(spacer_widget)        
        
        # 체크박스 4
        self.check_4 = CNV_CheckBox("부재")
        self.check_4.stateChanged.connect(self.toggle_4)
        self.check_4.setChecked(True)  # 체크박스 초기에 선택된 상태로 설정
        toolbar.addWidget(self.check_4)
        
        
        #메뉴바
        #file_menu.addAction(action_save)     
    #-----------------------------------------------------------
    #-----------------------------------------------------------
    # '현황측량도'파일 불러오기 버튼들 눌렀을 때 실행되는 함수
    def action_dxf_open_click_1(self):

        self.filenames, self.filter_string = QFileDialog.getOpenFileNames(self, caption="Open DXF File",
                                                                filter="DXF files (*.dxf)")

        for file in self.filenames:
            if os.path.isfile(file):
                try:
                    self.load_dxf_file_1(file)
                except:
                    pass
        
    #-----------------------------------------------------------
    # '현황측량도'파일을 로드하는 함수
    def load_dxf_file_1(self, filename):
        doc_1 = ezdxf.readfile(filename)
        self.dxf_1 = doc_1
        self.dxf_1_layers=self.load_dxf_layers(doc_1)
        self.input_dxf_layer_topo_widget(self.dxf_1_layers)#콤보박스에 리스트업

        self.view_ksh_01_topo.file_path_label_1.setText(f"파일 경로: {filename}")
        print(doc_1)
        print(self.dxf_1_layers)
        
        return doc_1
    #-----------------------------------------------------------
    # '터파기'파일 불러오기 버튼들 눌렀을 때 실행되는 함수
    def action_dxf_open_click_2(self):

        self.filenames, self.filter_string = QFileDialog.getOpenFileNames(self, caption="Open DXF File",
                                                                filter="DXF files (*.dxf)")

        for file in self.filenames:
            if os.path.isfile(file):
                try:
                    self.load_dxf_file_2(file)
                except:
                    pass
        
    #-----------------------------------------------------------
    # '터파기'파일을 로드하는 함수
    def load_dxf_file_2(self, filename):
        doc_2 = ezdxf.readfile(filename)
        self.dxf_2 = doc_2
        self.dxf_2_layers=self.load_dxf_layers(doc_2)
        self.input_dxf_layer_digging_widget(self.dxf_2_layers)#콤보박스에 리스트업

        self.view_ksh_01_topo.file_path_label_2.setText(f"파일 경로: {filename}")
        print(doc_2)
        print(self.dxf_2_layers)
        
        return doc_2    
    #-----------------------------------------------------------
    # '굴착계획평면도'파일 불러오기 버튼들 눌렀을 때 실행되는 함수
    def action_dxf_open_click_3(self):

        self.filenames, self.filter_string = QFileDialog.getOpenFileNames(self, caption="Open DXF File",
                                                                filter="DXF files (*.dxf)")

        for file in self.filenames:
            if os.path.isfile(file):
                try:
                    self.load_dxf_file_3(file)
                except:
                    pass
        
    #-----------------------------------------------------------
    # '굴착계획평면도'파일을 로드하는 함수
    def load_dxf_file_3(self, filename):
        doc_3 = ezdxf.readfile(filename)
        self.dxf_3 = doc_3
        self.dxf_3_layers=self.load_dxf_layers(doc_3)
        self.input_dxf_layer_pile_widget(self.dxf_3_layers)#콤보박스에 리스트업
        self.input_dxf_layer_mudblock_widget(self.dxf_3_layers)#콤보박스에 리스트업
        self.input_dxf_layer_bracing_widget(self.dxf_3_layers)#콤보박스에 리스트업
        self.input_dxf_layer_board_widget(self.dxf_3_layers)#콤보박스에 리스트업
        
        
        
        self.view_ksh_01_topo.file_path_label_3.setText(f"파일 경로: {filename}")
        print(doc_3)
        print(self.dxf_3_layers)
        
        return doc_3    
    
    #-----------------------------------------------------------
    #-----------------------------------------------------------
    # dxf 파일의 레이어 리스트 추출 메소드

    def load_dxf_layers(self, doc):

        try:

            layers = [layer.dxf.name for layer in doc.layers]
            layers.sort()  #레이어 리스트를 텍스트의 오름차순으로 정렬          
            return layers

        except IOError:

            print(f"Cannot open file")

            return []

        except ezdxf.DXFStructureError:

            print(f"Invalid or corrupted DXF file")

            return []
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    # '현황측량도'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_topo_widget(self,layerList):
        print(layerList)
        rowCount = 3
        self.view_ksh_01_topo.topo_table.setRowCount(rowCount)
        self.view_ksh_01_topo.topo_table.setItem(0,0, QTableWidgetItem("지형 레벨 포인트"))
        self.view_ksh_01_topo.topo_table.setItem(1,0, QTableWidgetItem("대지경계선"))
        self.view_ksh_01_topo.topo_table.setItem(2,0, QTableWidgetItem("보링점"))
        
        for i in range(self.view_ksh_01_topo.topo_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_01_topo.topo_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_01_topo.topo_table.rowCount()):
            item = self.view_ksh_01_topo.topo_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)

    # '터파기'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_digging_widget(self,layerList):
        print(layerList)
        rowCount = 2
        self.view_ksh_02_digging.digging_table.setRowCount(rowCount)
        self.view_ksh_02_digging.digging_table.setItem(0,0, QTableWidgetItem("지형 레벨 포인트"))
        self.view_ksh_02_digging.digging_table.setItem(1,0, QTableWidgetItem("대지경계선"))

        for i in range(self.view_ksh_02_digging.digging_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_02_digging.digging_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_02_digging.digging_table.rowCount()):
            item = self.view_ksh_02_digging.digging_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            
    # '파일'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_pile_widget(self,layerList):
        print(layerList)
        rowCount = 3
        self.view_ksh_03_material.pile_table.setRowCount(rowCount)
        self.view_ksh_03_material.pile_table.setItem(0,0, QTableWidgetItem("PRD"))
        self.view_ksh_03_material.pile_table.setItem(1,0, QTableWidgetItem("RCD"))
        self.view_ksh_03_material.pile_table.setItem(2,0, QTableWidgetItem("PHC"))

        for i in range(self.view_ksh_03_material.pile_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_03_material.pile_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_03_material.pile_table.rowCount()):
            item = self.view_ksh_03_material.pile_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            
    # '흙막이'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_mudblock_widget(self,layerList):
        print(layerList)
        rowCount = 4
        self.view_ksh_03_material.mudblock_table.setRowCount(rowCount)
        self.view_ksh_03_material.mudblock_table.setItem(0,0, QTableWidgetItem("CIP"))
        self.view_ksh_03_material.mudblock_table.setItem(1,0, QTableWidgetItem("PILE"))
        self.view_ksh_03_material.mudblock_table.setItem(2,0, QTableWidgetItem("H-PILE"))
        self.view_ksh_03_material.mudblock_table.setItem(3,0, QTableWidgetItem("슬러리월"))
        
        for i in range(self.view_ksh_03_material.mudblock_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_03_material.mudblock_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_03_material.mudblock_table.rowCount()):
            item = self.view_ksh_03_material.mudblock_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)            
            
    # '버팀대'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_bracing_widget(self,layerList):
        print(layerList)
        rowCount = 4
        self.view_ksh_03_material.bracing_table.setRowCount(rowCount)
        self.view_ksh_03_material.bracing_table.setItem(0,0, QTableWidgetItem("센터파일"))
        self.view_ksh_03_material.bracing_table.setItem(1,0, QTableWidgetItem("어스앵커"))
        self.view_ksh_03_material.bracing_table.setItem(2,0, QTableWidgetItem("스트러트"))
        self.view_ksh_03_material.bracing_table.setItem(3,0, QTableWidgetItem("띠장"))
        
        for i in range(self.view_ksh_03_material.bracing_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_03_material.bracing_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_03_material.bracing_table.rowCount()):
            item = self.view_ksh_03_material.bracing_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            
    # '복공판'레이어 리스트를 지형 레이어 콤보박스에 밀어넣는 작업
    def input_dxf_layer_board_widget(self,layerList):
        print(layerList)
        rowCount = 2
        self.view_ksh_03_material.board_table.setRowCount(rowCount)
        self.view_ksh_03_material.board_table.setItem(0,0, QTableWidgetItem("지형 레벨 포인트"))
        self.view_ksh_03_material.board_table.setItem(1,0, QTableWidgetItem("대지경계선"))

        for i in range(self.view_ksh_03_material.board_table.rowCount()):
            combo = CNV_ComboBox()
            combo.addItems(layerList)
            self.view_ksh_03_material.board_table.setCellWidget(i, 1, combo)
        
        #첫 번째 열의 아이템 수정 불가능하게 설정
        for i in range(self.view_ksh_03_material.board_table.rowCount()):
            item = self.view_ksh_03_material.board_table.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)            
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    # ---dd





    # 지형 작성 액션 메소드
    def action_generate_topo(self):
        
        # 현재 선택된 레벨포인트용 레이어
        current_level_layer = self.view_ksh_01_topo.topo_table.cellWidget(0,1).currentText()
        current_boring_layer = self.view_ksh_01_topo.topo_table.cellWidget(2,1).currentText()

        # current_level_layer의 이름을 가진 dxf파일 내의 레이어의 좌표를 가져오고 그것을 담을 리스트에 저장
        # DXF 파일을 읽음
        msp = self.dxf_1.modelspace()

        # 중복을 제거하기 위한 표면좌표 집합
        unique_coordinates = set()
        
        # 중복을 제거하기 위한 보링점 집합
        unique_boring = set()
        

        # 지정된 레이어의 모든 객체를 순회
        for entity in msp.query(f'*[layer=="{current_level_layer}"]'):
            if entity.dxftype() == 'LINE':
                # 선의 시작점과 끝점 좌표 추출
                start = entity.dxf.start
                end = entity.dxf.end
                nearest_text = find_nearest_text(msp,(start.x + end.x) / 2,(start.y + end.y) / 2)   
                point_z =0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = (start.z+end.z)/2
                       
                # 중심점 좌표 계산
                center = ((start.x + end.x) / 2, (start.y + end.y) / 2, point_z)
                unique_coordinates.add(center)

            elif entity.dxftype() == 'POINT':
            # 점의 좌표 추출
                nearest_text = find_nearest_text(msp,entity.dxf.location.x, entity.dxf.location.y)   
                point_z =0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = entity.dxf.location.z
                point = (entity.dxf.location.x, entity.dxf.location.y, point_z)
                unique_coordinates.add(point)

            elif entity.dxftype() == 'INSERT':
            # 삽입점 좌표 추출
                nearest_text = find_nearest_text(msp,entity.dxf.insert.x, entity.dxf.insert.y)   
                point_z = 0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = entity.dxf.insert.x

                insertion_point = (entity.dxf.insert.x, entity.dxf.insert.y,point_z)
                unique_coordinates.add(insertion_point)
            # 여기에 다른 DXF 객체 타입에 대한 처리를 추가할 수 있습니다.

        # 보링점 찾아서 넣을것임
        # 지정된 레이어의 모든 객체를 순회
        for entity in msp.query(f'*[layer=="{current_boring_layer}"]'):
            if entity.dxftype() == 'LINE':
                # 선의 시작점과 끝점 좌표 추출
                start = entity.dxf.start
                end = entity.dxf.end
                nearest_text = find_nearest_text(msp,(start.x + end.x) / 2,(start.y + end.y) / 2)   
                point_z =0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = (start.z+end.z)/2
                       
                # 중심점 좌표 계산
                center = ((start.x + end.x) / 2, (start.y + end.y) / 2, point_z)
                unique_boring.add(center)
                unique_coordinates.add(center)

            elif entity.dxftype() == 'POINT':
            # 점의 좌표 추출
                nearest_text = find_nearest_text(msp,entity.dxf.location.x, entity.dxf.location.y)   
                point_z =0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = entity.dxf.location.z
                point = (entity.dxf.location.x, entity.dxf.location.y, point_z)
                unique_boring.add(point)
                unique_coordinates.add(center)


            elif entity.dxftype() == 'INSERT':
            # 삽입점 좌표 추출
                nearest_text = find_nearest_text(msp,entity.dxf.insert.x, entity.dxf.insert.y)   
                point_z = 0
                try:
                    point_z = float(nearest_text)
                except:
                    point_z = entity.dxf.insert.x

                insertion_point = (entity.dxf.insert.x, entity.dxf.insert.y,point_z)
                unique_boring.add(insertion_point)
                unique_coordinates.add(center)

            # 여기에 다른 DXF 객체 타입에 대한 처리를 추가할 수 있습니다.

        # 집합을 출력
        top_coordinates_list = list(unique_coordinates)
        top_boring_list = list(unique_boring)

        print(top_coordinates_list)
        print(top_boring_list)

        
        
        try:
                data = {
                            "type": "create_topo",
                            "message": top_coordinates_list
                        }

                # JSON으로 직렬화
                json_data = json.dumps(data)

                # 소켓 설정 및 연결
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('localhost', 9989))

                # JSON 데이터 전송
                client_socket.sendall(json_data.encode('utf-8'))
                client_socket.close()






        except Exception as e:
            print(f"Error:{e}")
        

        
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