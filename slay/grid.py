import numpy as np
from math import sin, cos, pi
from abc import ABC, abstractmethod
from typing import Tuple

# TODO: Combine necessary classes (probably Grid, Tile, Piece, Region) into a rendering class
#       Will need to write render specific functions for each of these classes, would be nice
#       to delineate which class functions are specific to rendering

# TODO: In addition to render class, need interactive class to allow for a player interacting
#       with the game screen, change window size, etc. Generalize this class to an agent class
#       without necessity for screen action, but which can take commands from external AI
#       agent. In other words, screen interaction and AI decisions are just two different
#       versions of an agent's "get_next_action()" function (or something along these lines).

class Grid(ABC):
    '''
    A grid is the background set of points which are drawn to the screen. This just sets up
    the correct coordinates for rendering.
    '''

    def __init__(self, rows: int = 1, 
                       cols: int = 1, 
                       top_left: Tuple[float, float]=(0, 0), 
                       scale: float = 1):
        self.rows = rows
        self.cols = cols
        self.top_left = top_left
        self.scale = scale

    @property
    @abstractmethod
    def grid(self):
        pass

    def get(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        if coord[0] < 0 or coord[0] >= self.rows or coord[1] < 0 or coord[1] >= self.cols:
            raise ValueError(f"Tried to access invalid coordinates: {coord}")
        else:
            return self.grid[coord[0]][coord[1]]

class HexGrid(Grid):
    '''
    A hexagonal grid. Points are aligned along rows and shifted in alternating rows,
    forming equilateral triangles between neighboring points.
    '''

    grid = None

    def __init__(self, rows, cols, top_left, scale):
        super().__init__(rows=rows, cols=cols, top_left=top_left, scale=scale)

        self.grid = self.make_hex_grid(top_left=self.top_left, side_length=self.scale)
    
    def make_horizontal_line(self, left_pos=(0, 0), side_length=1):
        return [(left_pos[0] + x*side_length, left_pos[1]) for x in range(self.cols)]

    def make_hex_grid(self,top_left=(0, 0), side_length=1):
        def dx(i):
            if i % 2 == 0:
                return 0
            else:
                return cos(5*pi/3)*side_length
        def dy(i):
            return i*sin(5*pi/3)*side_length
        return [self.make_horizontal_line((top_left[0]+dx(i), top_left[1]-dy(i)), side_length)
            for i in range(self.rows)]