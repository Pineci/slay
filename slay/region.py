from tile import Tile
from typing import List, Tuple
from pieces import Piece
from map import Map
from queue import PriorityQueue

class Region:
    '''
    A region is a contiguous part of the playboard, i.e. connected tiles all of the same type.
    Essentially, it is a subset of the map with additionl information to keep track of the game pieces and rules
    '''

    # TODO: Change this class so that the tiles of a region are just represented by their coordinates,
    #       access actual hexagons through a map class
    def __init__(self, map: Map=None, tile_coords: List[Tuple[int, int]] = [], initialize: bool=True):
        self.map = map
        self.tile_coords = tile_coords
        self.pieces = []
        
        if initialize:
            self.initialize_region()

    def add_tile(self, tile_coord: Tuple[int, int]) -> None:
        if not self.contains_tile(tile_coord):
            self.tile_coords.append(tile_coord)

    def remove_tile(self, tile_coord: Tuple[int, int]) -> None:
        if self.contains_tile(tile_coord):
            self.tile_coords.remove(tile_coord)

    def contains_tile(self, tile_coord: Tuple[int, int]) -> bool:
        return tile_coord in self.tile_coords

    # TODO: Need to implement this, i.e. set balances etc.
    def initialize_region(self):
        pass

    # TODO: Implement this function properly so it maintains invariances
    def merge_regions(self, other: 'Region'):
        pass

    def check_valid_region(self) -> bool:
        return self.check_tile_same_team() and self.check_tile_connectivity() and self.check_piece_containment()

    def check_tile_connectivity(self) -> bool:
        if len(self.tiles > 1):
            reached = {coord: False for coord in self.tile_coords}
            queue = PriorityQueue()
            queue.put((0, self.tile_coords[0]))
            while queue.not_empty():
                priority, tile_coord = queue.get()
                tile = self.map.get_tile(tile_coord)
                neighbor_coords = tile.get_neighbors_coords()
                for coord in neighbor_coords:
                    if coord in self.tile_coords:
                        reached[coord] = True
                        queue.put((priority+1, coord))
            for coord in self.tile_coords:
                if not reached[coord]:
                    return False
        return True

    def check_tile_same_team(self) -> bool:
        if len(self.tiles >= 1):
            team = self.tiles[0].team
            for idx in range(1, len(self.tiles)):
                if self.tiles[idx].team != team:
                    return False
        return True

    def check_piece_containment(self) -> bool:
        ...