import pandas as pd
import folium
from branca.element import Figure
import math

train_df = pd.read_csv("data/train.csv")
#data_info_df = pd.read_csv('data_info.csv')
#test_df = pd.read_csv("test.csv")

dropped_train_df = train_df.drop(["road_name", "base_date", "day_of_week", "base_hour", "lane_count", "road_rating",
                                  "multi_linked", "connect_code", "height_restricted", "road_type", "start_turn_restricted", "end_turn_restricted", "vehicle_restricted"], axis=1)

# 훈련데이터 전체 차량에 대한 평균속도(v_0)는 42.78844km/h 이다.

# 위도 경도를 통한 변위 D 구하기

vol = 4701217
v_0 = 42.78844

list_X = []
list_Y = []
list_D = []
list_T = []  # D를 v_0으로 나눈 값
list_complexity = []
D_divide_target_T = []

for i in range(vol):
  X = ((math.cos(dropped_train_df.iloc[i,5])) * 6400*2*(math.pi)/360 ) * (abs((dropped_train_df.iloc[i,4]-dropped_train_df.iloc[i,7])))
  list_X.append(X)

for i in range(vol):
  Y = 6400*2*(math.pi)/360 * abs((dropped_train_df.iloc[i,5]-dropped_train_df.iloc[i,8]))
  list_Y.append(Y)

for i in range(vol):
  D = math.sqrt((list_X[i])**2 + (list_Y[i])**2)
  list_D.append(D)

for i in range(vol):
  list_T.append(list_D[i] / v_0)

for i in range(vol):
  D_divide_target_T.append(list_D[i] / dropped_train_df.iloc[i,9])

for i in range(vol):
  if (D_divide_target_T[i] > list_T[i]):
    list_complexity.append(1)     # 도로교통량 복잡, 많음
  else:
    list_complexity.append(0)  # 도로교통량 원활


# list_complexity를 dropped_train_df에 열로 추가할 거임.
dropped_train_df["complexity"] = list_complexity

###################
list_X_map = []
list_Y_map = []

for i in range(vol):
    X_map = abs((dropped_train_df.iloc[i, 4] + dropped_train_df.iloc[i, 7]) / 2)
    list_X_map.append(X_map)

for i in range(vol):
    Y_map = abs((dropped_train_df.iloc[i, 5] + dropped_train_df.iloc[i, 8]) / 2)
    list_Y_map.append(Y_map)

fig = Figure(width=550, height=350)
m = folium.Map(location=[33.3996213, 126.530975], zoom_start=9.5)

# folium.Marker([list_X_map[0], list_Y_map[0]], icon=folium.Icon('blue')).add_to(m)  # 원활

for i in range(vol):
    if (dropped_train_df.iloc[i, 10] == 0):
        folium.Marker([list_X_map[i], list_Y_map[i]], icon=folium.Icon('blue')).add_to(m)  # 원활
    elif (dropped_train_df.iloc[i, 10] == 1):
        folium.Marker([list_X_map[i], list_Y_map[i]], icon=folium.Icon('red')).add_to(m)  # 혼잡

m.save("jeju_map.html")

print("런 성공")