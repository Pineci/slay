from abc import ABC, abstractmethod
from typing import List, Tuple
from enum import Enum

class TileType(Enum):
    HEXAGON = "hexagon"

class Tile(ABC):

    def __init__(self, coords: Tuple[int, int] = (0, 0), 
                       active: bool = True, 
                       team: int = -1):
        self.tile_coords = coords # coordinates are (row, col)
        self.active = active
        self.team = team
    
    @abstractmethod
    def get_grid_coords(self) -> Tuple[int, int]:
        # Converts from tile coordinates to the coordinate of the upper left corner
        # of the shape on a corresponding grid.
        pass

    #TODO: Correct type signature
    @abstractmethod
    def get_shape_from_grid(self):
        pass

    @abstractmethod
    def get_neighbors_coords(self) -> List[Tuple[int, int]]:
        # Get coordinates of neighboring tiles in tile coordinate space
        pass

    def get_tile_coords(self) -> Tuple[int, int]:
        return self.tile_coords

    def set_activity(self, active: bool=True) -> None:
        self.active = active

    def set_team(self, team: int=-1) -> None:
        if self.is_active():
            self.team = team
        else:
            self.team = -1
    def get_team(self) -> int:
        return self.team

    def get_shape(self, grid):
        return self.get_shape_from_grid(grid, self.get_grid_coords(), use_grid=True)

    def is_neighbor(self, tile: 'Tile') -> bool:
        return tile.get_tile_coords() in self.get_neighbors_coords()

    def is_active(self) -> bool:
        return self.active

    def is_active_neighbor(self, tile: 'Tile') -> bool:
        return tile.is_active() and self.is_neighbor(tile)

    def __eq__(self, other: 'Tile') -> bool:
        return self.tile_coords == other.tile_coords

    @classmethod
    def get_tile_constructor(cls, type: TileType = TileType.HEXAGON):
        if type == TileType.HEXAGON:
            return Hexagon

class Hexagon(Tile):

    def __init__(self, coords: Tuple[int, int] = (0, 0), 
                       active: bool = True, 
                       team: int = -1):
        super().__init__(coords=coords, active=active, team=team)

    def get_grid_coords(self):
        row, col = self.tile_coords
        return (row, 1 + col*3 + (row % 2))

    def get_shape_from_grid(self, hex_grid, top_left=(0, 0), use_grid=True):
        if top_left[0] % 2 == 0:
            vertices = [[0, 0], [0, 1], [1, 1], [2, 1], [2, 0], [1, -1]]
            center = [1, 0]
        else:
            vertices = [[0, 0], [0, 1], [1, 2], [2, 1], [2, 0], [1, 0]]
            center = [1, 1]
        vertices = [[vertex[0] + top_left[0], vertex[1] + top_left[1]] for vertex in vertices]
        center = [top_left[0]+center[0], top_left[1] + center[1]]

        if use_grid:
            return list(map(lambda c: hex_grid.get(c), vertices)), hex_grid.get(center)
        else:
            return vertices, center

    def get_neighbors_coords(self):
        if self.tile_coords[0] % 2 == 0:
            relative_coords = [(-2, 0), (-1, 0), (1, 0), (2, 0), (1, -1), (-1, -1)]
        else:
            relative_coords = [(-2, 0), (-1, 1), (1, 1), (2, 0), (1, 0), (-1, 0)]
        return list(map(lambda c: (c[0] + self.tile_coords[0], c[1] + self.tile_coords[1]), relative_coords))
    
   