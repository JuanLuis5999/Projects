# 🔢 Sudoku Solver with GUI

This project implements a Sudoku solver using a recursive backtracking algorithm and displays the solution using a graphical interface built with Tkinter.

You can input puzzles through command-line arguments, and the application will show the puzzle before and after solving it. If the puzzle has no solution, it will notify you.

---

## 🚀 Features

- ✅ Solves Sudoku puzzles using backtracking
- 💡 Displays the puzzle and the solution using a Tkinter-based GUI
- 🧠 Visual highlight of 3x3 boxes for better readability
- 💬 Command-line input (9 strings of 9 digits each)
- 🧪 Optional `--grading` mode for output testing (prints flat string instead of GUI)

---

## 🛠 Technologies Used

- Python 3.x
- Tkinter (for GUI)
- Recursive algorithms (backtracking)

---

## 📦 How to Run

### ▶️ With GUI

Run the program with 9 arguments (each representing a row). Use `0` for empty cells:

```bash
python sudoku.py 530070000 600195000 098000060 800060003 400803001 700020006 060000280 000419005 000080079
