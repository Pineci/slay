from typing import Tuple
from tile import Tile, TileType
import numpy as np
from queue import PriorityQueue

class Map:
    '''
    This class maintains the game state, i.e. a list of regions containing tile pieces,
    handles loading and saving of a map, map generation, etc.
    '''

    # TODO: Implement this class
    def __init__(self, path: str = "", 
                       land_points: int = 1, 
                       sea_points: int = 0, 
                       size : Tuple[int, int] = (1, 1),
                       tile_type : TileType = TileType.HEXAGON):
        self.path = path
        self.num_land_points = land_points
        self.num_sea_points = sea_points
        self.size = size # size in (rows, cols)
        self.tile_type = tile_type

    def make_map(self) -> None:
        #TODO: Make sure these points don't repeat

        # Generate list of all possible points (indexed by (row, col)) in the grid
        rows, cols = np.meshgrid(np.arange(self.size[0]), np.arange(self.size[1]))
        rows = rows.flatten()
        cols = cols.flatten()
        points = np.array([(rows[i], cols[i]) for i in range(self.size[0] * self.size[1])])

        # Select unique points for land and sea points
        
        sample = np.random.choice(np.arange(len(points)), size=self.num_land_points + self.num_sea_points, replace=False)
        selected_points = list(map(tuple, list(points[sample])))

        land_points = selected_points[:self.num_land_points]
        sea_points = selected_points[self.num_land_points:]

        # Make mapping of points
        tile_constructor = Tile.get_tile_constructor(self.tile_type)
        self.map_tiles = [[tile_constructor((i, j)) for j in np.arange(self.size[1])] for i in np.arange(self.size[0])]

        # Make land points active tiles, sea points inactive
        for point in land_points:
            i, j = point
            self.map_tiles[i][j].set_activity(True)
        for point in sea_points:
            i, j = point
            self.map_tiles[i][j].set_activity(False)

        # DEBUG
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.map_tiles[i][j].priority = 0

        # Set up priority queue for breadth-first expansion of land and sea points
        reached = [[False for j in np.arange(self.size[1])] for i in np.arange(self.size[0])]
        q = PriorityQueue()
        counter = 0
        #np.random.shuffle(selected_points)
        for point in selected_points:
            i,j = point
            q.put((0, counter, self.map_tiles[i][j]))
            counter += 1
            reached[i][j] = True
            
        
        while not q.empty():
            priority, order, tile = q.get()
            #print((priority, order))
            neighbor_coords = tile.get_neighbors_coords()
            #print(neighbor_coords)
            neighbor_coords = list(np.random.permutation(neighbor_coords))
            #print(neighbor_coords)
            for coord in neighbor_coords:
                i, j = coord
                if self.in_range(coord) and not reached[i][j]:
                    reached[i][j] = True
                    self.map_tiles[i][j].set_activity(tile.is_active())
                    self.map_tiles[i][j].priority = priority+1
                    q.put((priority+1, counter, self.map_tiles[i][j]))
                    counter += 1

    def get_tile(self, coord : Tuple[int, int]) -> Tile:
        row, col = coord
        return self.map_tiles[row][col]

    def save_map(self):
        pass

    def load_map(self):
        pass

    def in_range(self, tile_coords: Tuple[int, int]) -> bool:
        return tile_coords[0] >= 0 and tile_coords[0] < self.size[0] and \
               tile_coords[1] >= 0 and tile_coords[1] < self.size[1]