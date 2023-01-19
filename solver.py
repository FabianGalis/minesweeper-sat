from itertools import combinations #for combinations
from tabulate import tabulate #for printing the board

#board encoding:
#0-8: mines nearby
#9  : unknown space
#10 : known mine
board=[
    [9,9,9,9,9,9],
    [9,2,1,1,1,9],
    [9,1,0,0,1,1],
    [9,2,3,2,1,9],
    [9,9,9,9,9,9]
]
print("Initial board:\n")
print("Legend:\n0-8: mines nearby\n9  : unknown\n10 : known mine")
print(tabulate(board, tablefmt="grid"))

board_w=len(board[0])
board_h=len(board)

# DIMACS codification
def M(i,j): return  board_w**1 * i + board_w**0 * j + 1

# find unknown cells next to a cell at i,j
def unknown_neighbours(i,j):
  neighbours=[]
  for h in range(i-1,i+2):
    for w in range(j-1,j+2):
      if h<board_h and w<board_w and (board[h][w]>8): neighbours.append((h,w))
  return neighbours

def cell_clauses(i,j):
  neighbours=unknown_neighbours(i,j)
  cell_clauses=[]

  #at least one mine
  for combination in combinations([M(elem[0],elem[1]) for elem in neighbours],len(neighbours)-board[i][j]+1):
    cell_clauses.append(list(combination))

  #at most one mine
  for combination in combinations([-M(elem[0],elem[1]) for elem in neighbours], board[i][j]+1):
    cell_clauses.append(list(combination))

  return cell_clauses


def board_clauses(board):
  clauses=[]
  for i in range(board_h):
    for j in range(board_w):
    
      if board[i][j]<9:
        #add self as known safe cell
        clauses.append([-M(i,j)])
        #add surrounding constraints
        clauses+=cell_clauses(i,j)
      elif board[i][j]==10:
        #add self as mine cell
        clauses.append([M(i,j)])
  return clauses

def show_solution(model):
  print("\nSAT - consistent")
  print("Model:",model)
  print("Legend:\n0-8: mines nearby\n9  : unknown\n10 : known mine\nm  : found mine\ns  : found safe")
  for i in range(board_h):
    for j in range(board_w):
      if board[i][j]==9: board[i][j]='m' if M(i, j) in model else 's'

  print(tabulate(board, tablefmt="grid"))

#print(board_clauses(board))

s = Solver(name='cd')
s.append_formula(board_clauses(board))

if s.solve(): show_solution(s.get_model())
else: print("\nUNSAT - inconsistent")