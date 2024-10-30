import pygame
from window import *
from line import *
from point import *
from cell import *
from tkinter import Tk, BOTH, Canvas
from maze import *
import sys

def main():
    num_rows=12
    num_cols=12
    margin=50
    screen_x=1024
    screen_y=768
    cell_size_x=(screen_x - 2*margin)/num_cols
    cell_size_y = (screen_y - 2 * margin)/num_rows
    sys.setrecursionlimit(10000)
    win = Window(screen_x,screen_y)
    maze = Maze(margin,margin,num_rows,num_cols,cell_size_x,cell_size_y,win)
    is_solved=maze.solve()
    print(is_solved[0])
    if is_solved[0]:
        print(f"maze solved in {is_solved[1]} moves!")
    else:
        print('maze cannot be solved!')

    win.wait_for_close()


main()

