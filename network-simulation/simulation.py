import random
import time
import math
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt

# === INITIALIZATION BLOCK ===
Rbps = 1 * (10 ** 6)  # 1 Mbps
Rts = 40 * 8  # Rts = Cts = ACK = 40 Bytes
Data = 1500 * 8  # 1500 Bytes
DIFS = 1 * (10 ** (-6))  # 1 µs
SIFS = 0.5 * (10 ** (-6))  # 0.5 µs
Gamma = DIFS + 3 * SIFS + 3 * (Rts / Rbps) + (Data / Rbps)
Alpha = DIFS + SIFS + 2 * (Rts / Rbps)
Nodes = 10
Cols = 6
Rows = Nodes
Matrix = [[0] * Cols for _ in range(Rows)]

# === FUNCTION BLOCK ===
def add_elements(matrix, n):
    for i in range(len(matrix)):
        matrix[i][2] = [0, (2 ** n) - 1]

def update_backoff_range(row, n):
    row[2] = [0, (2 ** n) - 1]

def get_exponent(max_value):
    exponent = math.ceil(math.log2(max_value + 1)) + 1
    return min(exponent, 10)

# === INITIAL DATA BLOCK ===
for i in range(Rows):
    Matrix[i][0] = i + 1  # Node ID

for i in range(Rows):
    Matrix[i][1] = 0  # Packets sent

add_elements(Matrix, 4)

for i in range(Rows):
    min_range = Matrix[i][2][0]
    max_range = Matrix[i][2][1]
    Matrix[i][3] = random.randint(min_range, max_range)  # Backoff counter

for i in range(Rows):
    Matrix[i][4] = 0  # Collisions

for i in range(Rows):
    Matrix[i][5] = Gamma  # Start time

# === GUI BLOCK - INITIAL TABLE DISPLAY ===
root = tk.Tk()
root.title("Initial Result Matrix")
root.geometry("800x800")

frame = tk.Frame(root)
frame.grid(sticky='news')

canvas = tk.Canvas(frame, width=800, height=800)
canvas.grid(row=0, column=0)

scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scroll_y.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=scroll_y.set)

scroll_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
scroll_x.grid(row=1, column=0, sticky='ew')
canvas.configure(xscrollcommand=scroll_x.set)

data_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=data_frame, anchor='nw')

headers = ["Node", "Packets", "CW", "Backoff", "Collisions"]
for j, header in enumerate(headers):
    label = tk.Label(data_frame, text=header, borderwidth=1, relief="solid", width=15, height=3, bg="#00539C", fg="white")
    label.grid(row=0, column=j, padx=5, pady=5)

for i, row in enumerate(Matrix):
    for j, val in enumerate(row[:5]):
        label = tk.Label(data_frame, text=str(val), borderwidth=1, relief="solid", width=15, height=3, bg="lightblue")
        label.grid(row=i + 1, column=j, padx=5, pady=5)

data_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
root.mainloop()

# === SIMULATION BLOCK ===
time.sleep(2)
discrete_time = Gamma
counter_aux = 0

while all(row[1] < 1000 for row in Matrix):
    zeros = [i for i, row in enumerate(Matrix) if row[3] == 0]

    if len(zeros) == 1:
        discrete_time += Gamma
        for row in Matrix:
            row[5] += Gamma
        i = zeros[0]
        Matrix[i][3] = random.randint(Matrix[i][2][0] + 1, Matrix[i][2][1])
        Matrix[i][1] += 1
        counter_aux += 1

    elif len(zeros) > 1:
        for i in zeros:
            current_max = Matrix[i][2][1]
            exp = get_exponent(current_max)
            update_backoff_range(Matrix[i], exp)
            Matrix[i][3] = random.randint(Matrix[i][2][0] + 1, Matrix[i][2][1])
            Matrix[i][4] += 1
        for row in Matrix:
            row[5] += Alpha
        discrete_time += Alpha
        counter_aux += 1

    else:
        for row in Matrix:
            row[3] -= 1
            row[5] += DIFS
        discrete_time += DIFS
        counter_aux += 1

    if counter_aux == 2500 * Nodes:
        print(Matrix[0][:5])
        counter_aux = 0

# === FINAL TABLE DISPLAY ===
root = tk.Tk()
root.title("Final Result Matrix")
root.geometry("800x800")

frame = tk.Frame(root)
frame.grid(sticky='news')

canvas = tk.Canvas(frame, width=800, height=800)
canvas.grid(row=0, column=0)

scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scroll_y.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=scroll_y.set)

scroll_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
scroll_x.grid(row=1, column=0, sticky='ew')
canvas.configure(xscrollcommand=scroll_x.set)

data_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=data_frame, anchor='nw')

for j, header in enumerate(headers):
    label = tk.Label(data_frame, text=header, borderwidth=1, relief="solid", width=15, height=3, bg="#00539C", fg="white")
    label.grid(row=0, column=j, padx=5, pady=5)

for i, row in enumerate(Matrix):
    for j, val in enumerate(row[:5]):
        label = tk.Label(data_frame, text=str(val), borderwidth=1, relief="solid", width=15, height=3, bg="lightblue")
        label.grid(row=i + 1, column=j)
