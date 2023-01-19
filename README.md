# minesweeper-sat
A SAT-based Minesweeper solver

## Requirements:
*PySat toolkit*
The simplest way to get and start using PySAT is to install the latest stable release of the toolkit from PyPI:
!pip install python-sat

## How it works
Input data is a matrix that represents a minesweeper board.
*Board encoding:*
0-8: mines nearby
9  : unknown space
10 : known mine
