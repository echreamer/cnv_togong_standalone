import ezdxf
import math
import json
 
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





# 사용 예시
## dxf파일 로드
dxf_file = 'data/C00-100 현황측량도.dxf'

doc = ezdxf.readfile(dxf_file)
msp = doc.modelspace()

# 중복을 제거하기 위한 집합
unique_coordinates = set()

current_level_layer = 'point-1'
# 지정된 레이어의 모든 객체를 순회
for entity in msp.query(f'*[layer=="{current_level_layer}"]'):
    if entity.dxftype() == 'LINE':
        # 선의 시작점과 끝점 좌표 추출
        start = entity.dxf.start
        end = entity.dxf.end
                
        # 중심점 좌표 계산
        center = ((start.x + end.x) / 2, (start.y + end.y) / 2, float(find_nearest_text(msp,(start.x + end.x) / 2,(start.y + end.y) / 2)))
        
        unique_coordinates.add(center)
    elif entity.dxftype() == 'POINT':
    # 점의 좌표 추출
        point = (entity.dxf.location.x, entity.dxf.location.y, float(find_nearest_text(msp,entity.dxf.location.x,entity.dxf.location.y)))
        unique_coordinates.add(point)

    elif entity.dxftype() == 'INSERT':
    # 삽입점 좌표 추출
        insertion_point = (entity.dxf.insert.x, entity.dxf.insert.y,float(find_nearest_text(msp,entity.dxf.insert.x, entity.dxf.insert.y)))
        unique_coordinates.add(insertion_point)

    # 여기에 다른 DXF 객체 타입에 대한 처리를 추가할 수 있습니다.
# 보링점 찾아서 넣을것임



# 집합을 출력
unique_coordinates_list = list(unique_coordinates)
print(unique_coordinates_list)

