import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# 초기 변수 설정
glucose_concentration = st.sidebar.selectbox(
    "포도당 농도 (%)", 
    ["5%", "10%", "15%", "대조군"]
)
yeast_concentration = st.sidebar.slider("효모 농도 (g/L)", 0.1, 5.0, 1.0)
time_elapsed = st.sidebar.slider("시간 (분)", 0, 60, 0)
koh_added = st.sidebar.checkbox("수산화칼륨 추가")

# 이산화탄소 발생량 계산 함수
def calculate_co2(glucose, yeast, time):
    if glucose == "대조군":
        return 0
    glucose_val = int(glucose.replace('%', ''))
    return glucose_val * yeast * math.log1p(time)

# 이산화탄소 발생량 계산
co2_volume = calculate_co2(glucose_concentration, yeast_concentration, time_elapsed)

# 발효관 그리기 함수
def draw_fermentation_tube(co2_volume, glucose_concentration):
    fig, ax = plt.subplots(figsize=(3, 6))

    # 발효관 그림
    ax.add_patch(plt.Rectangle((0.4, 0.1), 0.2, 0.7, fill=None, edgecolor="black", linewidth=2))  # 발효관 몸체
    ax.add_patch(plt.Circle((0.5, 0.85), 0.1, fill=None, edgecolor="black", linewidth=2))  # 팽대부

    # 이산화탄소 표시
    if not koh_added:
        co2_height = co2_volume / 100  # 단순화된 시각화를 위해 크기 조정
        ax.add_patch(plt.Rectangle((0.4, 0.1), 0.2, co2_height, color="gray"))  # 맹관부의 이산화탄소

    # 맹관부 표시
    ax.text(0.5, 0.05, "맹관부", horizontalalignment='center', fontsize=12)

    # 축과 배경 제거
    ax.axis('off')
    st.pyplot(fig)

# 발효관 그림 그리기
st.write(f"포도당 농도: {glucose_concentration}, 효모 농도: {yeast_concentration} g/L, 시간: {time_elapsed} 분")
st.write(f"이산화탄소 발생량: {co2_volume:.2f} mL")
draw_fermentation_tube(co2_volume, glucose_concentration)

if koh_added:
    st.write("수산화칼륨이 추가되었습니다. CO2가 제거되었습니다.")
