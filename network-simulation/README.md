# 📡 Network Collision & Transmission Simulation

This Python-based simulation models the behavior of a network where multiple nodes attempt to transmit packets. The system simulates discrete time, detects collisions, and applies exponential backoff to resolve transmission conflicts. 

It includes a graphical interface built with Tkinter to show node states in real time, and matplotlib charts to analyze final results.

---

## 🚀 Features

- 📶 Simulates some network nodes transmitting over time
- 💥 Collision detection and exponential backoff
- ⏱ Discrete time simulation with delays and random backoff counters
- 📊 Real-time table display using Tkinter
- 📈 Final charts:
  - Collisions per node
  - Transmission rate per node (kbps)

---

## 🛠 Technologies Used

- Tkinter (for GUI table visualization)
- matplotlib (for graphing results)
- random, math, time

---

## 📦 How to Run

1. Clone this repository or download the folder
2. Install dependencies
3. Run the simulation
4. The app will display:
- Initial node status (Tkinter table)
- Real-time updates as nodes transmit
- Final results in charts after simulation completes

## 📸 Example Output



- Real-time node status:
*(Tkinter table shown during simulation)*

- Final graphs:
- 📊 Collisions vs Node
- ⚡ Transmission rate (kbps) vs Node


## 🧠 Purpose

This project helps visualize how packet collisions affect network throughput and how exponential backoff helps avoid constant interference. It simulates behavior similar to CSMA/CA or random access protocols in wireless networks.

Great for learning and teaching how low-level network protocols behave under load.

---

Created by JuanLuis5999 – 2023
