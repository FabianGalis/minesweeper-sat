from pysat.solvers import Solver #for SAT solving
from itertools import combinations #for combinations in a CNF
from tabulate import tabulate #for printing boards
from random import sample #for generating random boards
import matplotlib.pyplot as plt #for time analysis plotting
from time import time #for time analysis

def board_generator(board_w,board_h,mine_count):
  #empty board
  solved_b = [[0 for row in range(board_w)] for column in range(board_h)]

  #place random mines
  coords = sample([(i,j) for i in range(board_h) for j in range(board_w)],mine_count)

  #update board
  for i,j in coords:
    solved_b[i][j]=10
    if i>0 and j>0 and solved_b[i-1][j-1]<10:         solved_b[i-1][j-1]+=1
    if j>0 and solved_b[i][j-1]<10:                   solved_b[i][j-1]+=1
    if i<board_h-1 and j>0 and solved_b[i+1][j-1]<10: solved_b[i+1][j-1]+=1
    if i>0 and solved_b[i-1][j]<10:                   solved_b[i-1][j]+=1
    if i<board_h-1 and solved_b[i+1][j]<10:           solved_b[i+1][j]+=1
    if i>0 and j<board_w-1 and solved_b[i-1][j+1]<10: solved_b[i-1][j+1]+=1
    if j<board_w-1 and solved_b[i][j+1]<10:           solved_b[i][j+1]+=1
    if i<board_h-1 and j<board_w-1 and solved_b[i+1][j+1]<10: solved_b[i+1][j+1]+=1

  return solved_b

# marks some parts of the board as unknown cells 
def unsolved_board(board,unknown_count):
  coords = sample([(i,j) for i in range(len(board)) for j in range(len(board[0]))],unknown_count)
  for i,j in coords:
    board[i][j] = 9

  return board

# DIMACS codification
def M(i,j,board_w): return  board_w**1 * i + board_w**0 * j + 1

# find unknown cells next to a cell at i,j
def unknown_neighbours(board,i,j):
  neighbours=[]
  for h in range(i-1,i+2):
    for w in range(j-1,j+2):
      if h<len(board) and w<len(board[0]) and h>=0 and w>=0 and (board[h][w]>8): neighbours.append((h,w))
  return neighbours

# clauses per cell
def cell_clauses(board,i,j):
  neighbours=unknown_neighbours(board,i,j)
  cell_clauses=[]

  #at least n mines
  for combination in combinations([M(elem[0],elem[1],len(board[0])) for elem in neighbours],len(neighbours)-board[i][j]+1):
    cell_clauses.append(list(combination))

  #at most n mines
  for combination in combinations([-M(elem[0],elem[1],len(board[0])) for elem in neighbours], board[i][j]+1):
    cell_clauses.append(list(combination))

  return cell_clauses

# clauses per board
def board_clauses(board,board_h,board_w):
  clauses=[]
  for i in range(board_h):
    for j in range(board_w):
    
      if board[i][j]<9:
        #add self as known safe cell
        clauses.append([-M(i,j,board_w)])
        #add surrounding constraints
        clauses+=cell_clauses(board,i,j)
      elif board[i][j]==10:
        #add self as mine cell
        clauses.append([M(i,j,board_w)])
  return clauses

#print solution
def show_solution(board,board_h,board_w,model):
  for i in range(board_h):
    for j in range(board_w):
      if board[i][j]==9: board[i][j]='m' if M(i, j,board_w) in model else 's'

  #print(tabulate(board, tablefmt="grid"))
  return board
  

#print(board_clauses(board,board_h,board_w))
def solve_board(board,printing=True):
  if printing:
    print("Initial board:\n")
    print("Legend:\n0-8: mines nearby\n9  : unknown\n10 : known mine")
    print(tabulate(board, tablefmt="grid"))

  board_w=len(board[0])
  board_h=len(board)

  s = Solver(name='cd')
  s.append_formula(board_clauses(board,board_h,board_w))

  if s.solve():
    model=s.get_model()
    solved_board=show_solution(board,board_h,board_w,model)
    if printing:
      print("\nSAT - consistent")
      print("Model:",model)
      print("Legend:\n0-8: mines nearby\n9  : unknown\n10 : known mine\nm  : found mine\ns  : found safe")
      print(tabulate(solved_board, tablefmt="grid"))
    return True
  else:
    print("\nUNSAT - inconsistent")
    return False

#board encoding:
#0-8: mines nearby
#9  : unknown space
#10 : known mine

board_width=10
board_height=8
mine_count=15 #smaller than width*height
unknown_cells=40 #smaller than width*height
board=unsolved_board(board_generator(board_width,board_height,mine_count),unknown_cells)

# board=[
#     [9,9,9,9,9,9],
#     [9,2,1,1,1,9],
#     [9,1,0,0,1,1],
#     [9,2,3,2,1,9],
#     [9,9,9,9,9,9]
# ]

#solve_board(board)

#SCALING----------------------------------------------------------------------------------------------------


#SCALING FOR MINE COUNT
def scale_for_mines(mine_count_limit,fixed_board_size=100,fixed_unknown_cell_count=20):
  #elapsed[m] = time taken to solve board with m mines
  elapsed = [0 for mines in range(mine_count_limit)]

  for m in range(mine_count_limit):
    #print(m)
    board=unsolved_board(board_generator(fixed_board_size,fixed_board_size,m),fixed_unknown_cell_count)
    start=time()
    solve_board(board,False)
    elapsed[m]=time()-start
      
  return elapsed

#SCALING FOR SIZE
def scale_for_board_size(board_size_limit,fixed_mine_count=20,fixed_unknown_cell_count=20):
  #elapsed[w][h] = time taken to solve board of width w and height h
  elapsed = [[0 for row in range(board_size_limit)] for column in range(board_size_limit)]

  for i in range(5,board_size_limit):
    #print(i)
    for j in range(5,board_size_limit):
      board=unsolved_board(board_generator(i,j,fixed_mine_count),fixed_unknown_cell_count)
      start=time()
      solve_board(board,False)
      elapsed[i][j]=time()-start
      
  return elapsed

#SCALING FOR UNKNOWN CELL COUNT
def scale_for_unknown_cells(unknown_cell_count,fixed_board_size=100,fixed_mine_count=20):
  #elapsed[c] = time taken to solve board with c unknown cells
  elapsed = [0 for cells in range(unknown_cell_count)]

  for c in range(unknown_cell_count):
    #print(c)
    board=unsolved_board(board_generator(fixed_board_size,fixed_board_size,fixed_mine_count),unknown_cell_count)
    start=time()
    solve_board(board,False)
    elapsed[c]=time()-start
      
  return elapsed

def graph_scale_for_mines(elapsed):
  ax = plt.axes()
  ax.plot(range(len(elapsed)),elapsed)
  ax.set_xlabel("mines")
  ax.set_ylabel("time")
  plt.show()

def graph_scale_for_board_size(elapsed):
  ax = plt.axes(projection='3d')
  ax.plot3D(range(len(elapsed)),range(len(elapsed)), elapsed[10], label='time')
  ax.set_xlabel("w")
  ax.set_ylabel("h")
  ax.legend()
  plt.show()

def graph_scale_for_unknown_cells(elapsed):
  ax = plt.axes()
  ax.plot(range(len(elapsed)),elapsed)
  ax.set_xlabel("unknown cells")
  ax.set_ylabel("time")
  plt.show()

mines_limit=100
board_size_limit=30
unknown_cells_limit=100

#graph_scale_for_mines(scale_for_mines(mines_limit))
graph_scale_for_board_size(scale_for_board_size(board_size_limit))
#graph_scale_for_unknown_cells(scale_for_unknown_cells(unknown_cells_limit))
