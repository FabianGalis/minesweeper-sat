# minesweeper-sat
A SAT-based Minesweeper solver

Note that it works only for the "no guessing" gamemode.

## Requirements:
**PySat toolkit**

The simplest way to get and start using PySAT is to install the latest stable release of the toolkit from PyPI:

!pip install python-sat

## How it works
Input data is a matrix that represents a minesweeper board.

**Board encoding:**
- 0-8: mines nearby\n
- 9  : unknown space
- 10 : known mine
**Conversion to clauses**
- each cell represents a propositional variable;
- each variable is either true = there is a mine, or false = there's no mine;
- the clause set is initialised with the variables that are already known (the uncovered cells);
- the rest of the variables are put in clauses according to the nearby numbered cells.

The end result is either SAT, and the model represents the location of the mines nearby, or UNSAT, which means that the board is inconsistent.

In the end, the program generates the solved board, along with the position of the mines and free spaces.
