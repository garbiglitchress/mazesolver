import time
from cell import *
import random
class Maze:
    moves=0

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1=x1
        self._y1=y1
        self._num_rows=num_rows
        self._num_cols=num_cols
        self._cell_size_x=cell_size_x
        self._cell_size_y=cell_size_y
        self._win=win
        self._cells=[]
        self.moves=0
        if seed!=None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells=[]
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j)

            


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        
        x1=self._x1 + i*self._cell_size_x
        y1=self._y1+ j*self._cell_size_y
        x2=x1+self._cell_size_x
        y2=y1+self._cell_size_y
        self._cells[i][j].draw(x1,y1,x2,y2)
        self._animate(.01)

    def _animate(self, timer=.05):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(timer)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall=False
        self._draw_cell(0,0)

        self._cells[-1][-1].has_bottom_wall=False
        self._draw_cell(self._num_cols-1,self._num_rows-1)
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited=True
        while True:
            visiting=[]
            poss_directions=[]
            visit_indexes=[]
            if i>0:
                if not self._cells[i-1][j].visited:
                    visiting.append(self._cells[i-1][j])
                    poss_directions.append('L')
                    visit_indexes.append((i-1,j))
            if i<self._num_cols-1:
                if not self._cells[i+1][j].visited:
                    visiting.append(self._cells[i+1][j])
                    poss_directions.append('R')
                    visit_indexes.append((i+1,j))
            if j!=0:
                if not self._cells[i][j-1].visited:
                    visiting.append(self._cells[i][j-1])
                    poss_directions.append('U')
                    visit_indexes.append((i,j-1))
            if j!=self._num_rows-1:
                if not self._cells[i][j+1].visited:
                    visiting.append(self._cells[i][j+1])
                    poss_directions.append('D')
                    visit_indexes.append((i,j+1))
            #finish this later
            if len(visit_indexes)==0:
                self._draw_cell(i,j)
                return
            else:
                direction_index=random.randrange(len(visit_indexes))
                next_index=visit_indexes[direction_index]
                if next_index[0]==i+1:#r
                    self._cells[i][j].has_right_wall=False
                    self._cells[i+1][j].has_left_wall=False
                if next_index[0]==i-1:#l
                    self._cells[i][j].has_left_wall=False
                    self._cells[i-1][j].has_right_wall=False
                if next_index[1]==j+1:#d
                    self._cells[i][j].has_bottom_wall=False
                    self._cells[i][j+1].has_top_wall=False    
                if next_index[1]==j-1:#u
                    self._cells[i][j].has_top_wall=False
                    self._cells[i][j-1].has_bottom_wall=False    
                self._break_walls_r(next_index[0],next_index[1])
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited=False
    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        global moves
        self._animate()
        self._cells[i][j].visited=True
        if i==self._num_cols-1 and j==self._num_rows-1:
            return (True,self.moves)
        
        #check each direction
        #left
        if i!=0 and self._cells[i-1][j].visited==False and self._cells[i][j].has_left_wall==False:
            self.moves+=1
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1,j)[0]:
                return (True,self.moves)
            else:
                self.moves+=1
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        #up
        if i!=0 and self._cells[i][j-1].visited==False and self._cells[i][j].has_top_wall==False:
            self.moves+=1
            self._cells[i][j].draw_move(self._cells[i][j-1])
            
            if self._solve_r(i,j-1)[0]:
                return (True,self.moves)
            else:
                self.moves+=1
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        #right
        if i!=self._num_cols-1 and self._cells[i+1][j].visited==False and self._cells[i][j].has_right_wall==False:
            self.moves+=1
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1,j)[0]:
                return (True,self.moves)
            else:
                self.moves+=1
                self._cells[i][j].draw_move(self._cells[i+1][j], True)

        #down
        if j!=self._num_rows-1 and self._cells[i][j+1].visited==False and self._cells[i][j].has_bottom_wall==False:
            self.moves+=1
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i,j+1)[0]:
                return (True,self.moves)
            else:
                self.moves+=1
                self._cells[i][j].draw_move(self._cells[i][j+1], True)


        return (False, self.moves)