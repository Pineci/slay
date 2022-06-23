from typing import Tuple, List
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

        # Set up priority queue for breadth-first expansion of land and sea points
        reached = [[False for j in np.arange(self.size[1])] for i in np.arange(self.size[0])]
        q = PriorityQueue()
        counter = 0
        np.random.shuffle(selected_points)
        for point in selected_points:
            i,j = point
            q.put((0, counter, self.map_tiles[i][j]))
            counter += 1
            # TODO: remove this line
            self.map_tiles[i][j].priority = 0
            reached[i][j] = True
            
        
        while not q.empty():
            priority, order, tile = q.get()
            neighbor_coords = tile.get_neighbors_coords()
            neighbor_coords = list(np.random.permutation(neighbor_coords))
            for coord in neighbor_coords:
                i, j = coord
                if self.in_range(coord) and not reached[i][j]:
                    reached[i][j] = True
                    self.map_tiles[i][j].set_activity(tile.is_active())
                    # TODO: remove this line
                    self.map_tiles[i][j].priority = priority+1
                    q.put((priority+1, counter, self.map_tiles[i][j]))
                    counter += 1

    def get_tile(self, coord : Tuple[int, int]) -> Tile:
        row, col = coord
        return self.map_tiles[row][col]

    def __iter__(self):
        self.iter_i = 0
        self.iter_j = 0
        return self

    def __next__(self):
        i, j = self.iter_i, self.iter_j
        if self.iter_i >= self.size[0]:
            if self.iter_j >= self.size[1]:
                raise StopIteration
            else:
                self.iter_j += 1
                self.iter_i = 0
        else:
            self.iter_i += 1
        return self.get_tile((i, j))

    def __len__(self):
        return self.size[0] * self.size[1]

    def bfs_find_same_team(self, start_coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        if not self.in_range(start_coord):
            return []

        # Set up priority queue
        reached = [[False for j in np.arange(self.size[1])] for i in np.arange(self.size[0])]
        counter = 0

        q = PriorityQueue()
        q.put((0, counter, self.get_tile(start_coord)))
        reached[start_coord[i]][start_coord[j]] = True
        same_tiles = [start_coord]
        team = self.get_tile(start_coord).get_team()
            
        while not q.empty():
            priority, _, tile = q.get()
            neighbor_coords = tile.get_neighbors_coords()
            for coord in neighbor_coords:
                i, j = coord
                if self.in_range(coord) and not reached[i][j] and tile.get_team() == team:
                    reached[i][j] = True
                    same_tiles.append(coord)
                    q.put((priority+1, counter, self.get_tile(coord)))
                    counter += 1
        return same_tiles

    def save_map(self):
        pass

    def load_map(self):
        pass

    def in_range(self, tile_coords: Tuple[int, int]) -> bool:
        return tile_coords[0] >= 0 and tile_coords[0] < self.size[0] and \
               tile_coords[1] >= 0 and tile_coords[1] < self.size[1]