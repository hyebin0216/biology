import streamlit as st
import math

# 초기 변수 설정
glucose_concentration = st.sidebar.slider("포도당 농도 (%)", 5.0, 15.0, 5.0)
yeast_concentration = st.sidebar.slider("효모 농도 (g/L)", 0.1, 5.0, 1.0)
time_elapsed = st.sidebar.slider("시간 (분)", 0, 60, 0)
koh_added = st.sidebar.checkbox("수산화칼륨 추가")

# 이산화탄소 발생량 계산 함수
def calculate_co2(glucose, yeast, time):
    return glucose * yeast * math.log1p(time)

# 이산화탄소 발생량 계산
co2_volume = calculate_co2(glucose_concentration, yeast_concentration, time_elapsed)

# 이산화탄소 발생량 표시
st.write(f"이산화탄소 발생량: {co2_volume:.2f} mL")

if koh_added:
    st.write("수산화칼륨이 추가되었습니다. CO2가 제거되었습니다.")

# 시각화: 간단한 막대 그래프
st.bar_chart({
    "포도당 농도": [glucose_concentration],
    "효모 농도": [yeast_concentration],
    "이산화탄소 발생량": [co2_volume],
})
