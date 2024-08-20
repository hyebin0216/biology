import tkinter as tk
from tkinter import ttk
import math

# 기본 설정
root = tk.Tk()
root.title("퀴네 발효관 시뮬레이션")

# 초기 변수 설정
glucose_concentration = tk.DoubleVar(value=5.0)  # 포도당 농도 (%)
yeast_concentration = tk.DoubleVar(value=1.0)    # 효모 농도 (g/L) - 통제변인
time_elapsed = tk.IntVar(value=0)                # 시간 (분)
co2_volumes = {'5%': 0.0, '10%': 0.0, '15%': 0.0, '대조군': 0.0}  # 이산화탄소 발생량 (mL)
koh_added = tk.BooleanVar(value=False)           # 수산화칼륨 추가 여부

# 이산화탄소 발생량 계산 함수
def calculate_co2():
    yeast = yeast_concentration.get()
    time = time_elapsed.get()

    # 각 농도에 대한 이산화탄소 발생량 계산
    for concentration in co2_volumes.keys():
        if concentration != '대조군':
            glucose = float(concentration.replace('%', ''))
            co2_volumes[concentration] = glucose * yeast * math.log1p(time)
        else:
            co2_volumes[concentration] = 0  # 대조군은 포도당이 없으므로 CO2 발생 없음

    draw_fermentation_tubes()

# 발효관 그림 그리기 함수
def draw_fermentation_tubes():
    canvas.delete("all")
    tubes = ['5%', '10%', '15%', '대조군']
    positions = [50, 150, 250, 350]
    
    for i, tube in enumerate(tubes):
        # 발효관 그리기 (팽대부 포함)
        canvas.create_oval(positions[i], 10, positions[i] + 40, 60, outline="black", width=2)  # 팽대부
        canvas.create_rectangle(positions[i], 50, positions[i] + 40, 300, outline="black", width=2)  # 발효관 몸체
        canvas.create_rectangle(positions[i] + 10, 50, positions[i] + 30, 100, fill="blue", outline="black")  # 맹관부 (가득 찬 상태)
        canvas.create_text(positions[i] + 20, 40, text=f"{tube} 맹관부", fill="black", font=('Arial', 8))  # 맹관부 표시

        # 이산화탄소 표시
        co2_height = int(co2_volumes[tube] / 10)  # 단순히 시각적으로 나타내기 위해 10으로 나눔
        if co2_height > 200:
            co2_height = 200  # 맹관부의 최대 크기로 제한
        if not koh_added.get():
            canvas.create_rectangle(positions[i] + 10, 300 - co2_height, positions[i] + 30, 300, fill="gray")  # 맹관부의 이산화탄소
        else:
            canvas.create_text(positions[i] + 20, 280, text="CO2 제거됨", fill="red", font=('Arial', 8))  # CO2 제거 표시

        # 눈금 표시 및 숫자
        for j in range(0, 26):
            y = 300 - (j * 10)
            canvas.create_line(positions[i] + 30, y, positions[i] + 40, y, fill="black")  # 눈금선
            if j % 5 == 0:
                canvas.create_text(positions[i] + 50, y, text=str(j * 10), fill="black", font=('Arial', 8))  # 눈금 숫자

# 수산화칼륨 추가 함수
def add_koh():
    koh_added.set(True)
    draw_fermentation_tubes()

# GUI 요소 배치
ttk.Label(root, text="포도당 농도 (%):").grid(column=0, row=0, padx=10, pady=10)
glucose_options = ttk.Combobox(root, textvariable=glucose_concentration, values=[5.0, 10.0, 15.0], state="readonly")
glucose_options.grid(column=1, row=0, padx=10, pady=10)
glucose_options.bind("<<ComboboxSelected>>", lambda event: calculate_co2())

ttk.Label(root, text="효모 농도 (g/L):").grid(column=0, row=1, padx=10, pady=10)
ttk.Scale(root, from_=0.1, to=5.0, variable=yeast_concentration, command=lambda x: calculate_co2()).grid(column=1, row=1, padx=10, pady=10)

ttk.Label(root, text="시간 (분):").grid(column=0, row=2, padx=10, pady=10)
ttk.Scale(root, from_=0, to=60, variable=time_elapsed, command=lambda x: calculate_co2()).grid(column=1, row=2, padx=10, pady=10)

ttk.Button(root, text="수산화칼륨 추가", command=add_koh).grid(column=0, row=3, columnspan=2, pady=10)

# 캔버스에 발효관 그리기
canvas = tk.Canvas(root, width=480, height=350, bg="white")
canvas.grid(column=2, row=0, rowspan=5, padx=10, pady=10)

# 초기 발효관 그리기
draw_fermentation_tubes()

# 시뮬레이션 시작
calculate_co2()
root.mainloop()
