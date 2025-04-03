import sys
import time
from tkinter import*


def is_bad(sudoku, row, col, x):

    boxrow=row-(row%3)
    boxcol=col-(col%3)

    for i in range(9):
    	if x==sudoku[i][col]:
    		return True
  	
    for j in range(9):
    	if x==sudoku[row][j]:
   			return True
   			
    boxrow=row-(row%3)
    bowcol=col-(col%3)
    
    for k in range(3):
    	for l in range(3):
    		if x==sudoku[boxrow+k][boxcol+l]:
    			return True
    return False
        
def solve_sudoku(sudoku):
    cell=find_empy_cell(sudoku)
    if cell==None:
    	return True

    [row,col]=cell
    
    for i in range(1,10):
    	if not is_bad(sudoku,row,col,i):
    		sudoku[row][col]=i
    		if solve_sudoku(sudoku):
    			return True
    	
    	sudoku[row][col]=0	
   
    return False

def find_empy_cell(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return [i,j]
    return None

def parse_from_args(args):
    sudoku = [[0 for i in range(9)] for j in range(9)]
    for i in range(1, len(args)):
        if args[i] == '--grading':
            continue
        if len(args[i]) != 9:
            print("Invalid format in argument " + str(i+1))
            return None
        for j in range(9):
            sudoku[i-1][j] = int(args[i][j])
    return sudoku
            
def print_sudoku(sudoku):
	window=Tk()
	window.title("Sudoku")
	window.geometry("1275x690")
	window.config(bg="green")
	

	rows = []
	for i in range(9):
		cols = []
		for j in range(9):
			add = Entry(window,relief=GROOVE,width=5,font='Consolas 20',fg='black',justify='center',background='pink')
			add.grid(row=i, column=j, sticky=NSEW, ipadx=10, ipady=10)
			if(sudoku[i][j]==0):
				a=' '
			if(sudoku[i][j]!=0):
				a=sudoku[i][j]
			add.insert(END, a)
			if((j+1)%3==0):
				add.grid(row=i, column=j, padx=(0,20))
			if((i+1)%3==0):
				add.grid(row=i, column=j, pady=(0,20))	
				
			cols.append(add)	
		rows.append(cols)
	window.mainloop()
	
def print_simple(sudoku):
    s = ''
    for x in range(len(sudoku)):
        for y in range(len(sudoku[0])):
            s += str(sudoku[x][y])
    print(s)

if __name__ == '__main__':
    if len(sys.argv) < 10:
        print("Too few parameteres.")
        exit()
    sudoku = parse_from_args(sys.argv)
    if '--grading' in sys.argv:
        if not solve_sudoku(sudoku):
            print("Cannot solve sudoku")
        print_simple(sudoku)
        exit()
       
    print_sudoku(sudoku)
    if not solve_sudoku(sudoku):
        print("Cannot solve sudoku")
    print("")
    print_sudoku(sudoku)
