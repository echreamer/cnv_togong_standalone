from sklearn.linear_model import LinearRegression

# 첫 번째 지층면 데이터
topo_xyzs = [(1,1,10),(1,2,11),(1,3,10),(1,4,15),(1,5,9),(2,1,11),(2,2,13),(2,3,20),(2,4,15),(2,5,10),(3,1,30),(3,2,10),(3,3,15),(3,4,16),(3,5,13),(4,1,30),(4,2,10),(4,3,15),(4,4,16),(4,5,13),(5,1,33),(5,2,10),(5,3,11),(5,4,13),(5,5,10)]

# x, y 좌표 추출
X_train = [(x, y) for x, y, _ in topo_xyzs]

# z 값 추출
z_train = [z for _, _, z in topo_xyzs]

# 선형 회귀 모델 훈련
model = LinearRegression()
model.fit(X_train, z_train)

# 두 번째 지층면 데이터
point_xyzs = [(2,3.3,15),(3.2,5.3,10),(5.1,2.3,6)]

# x, y 좌표 추출
X_test = [(x, y) for x, y, _ in point_xyzs]

# 두 번째 지층면 z 값 예측
z_pred = model.predict(X_test)

# 결과 출력
for i in range(len(point_xyzs)):
    print(f"두 번째 지층면 좌표: {point_xyzs[i]}, 예측된 z 값: {z_pred[i]}")
