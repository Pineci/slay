from tile import Tile
from typing import List, Tuple
from piece import *
from map import Map
from queue import PriorityQueue
import numpy as np

class RegionConfig:

    tile_starting_balance = 5

class Region:
    '''
    A region is a contiguous part of the playboard, i.e. connected tiles all of the same type.
    Essentially, it is a subset of the map with additionl information to keep track of the game pieces and rules
    '''

    def __init__(self, map: Map=None, tile_coords: List[Tuple[int, int]] = [], initialize: bool=True, id: int=0):
        self.map = map
        self.tile_coords = tile_coords
        self.pieces = {}
        self.id = id
        
        if initialize:
            self.initialize_region()

    def __eq__(self, other: 'Region') -> bool:
        return self.id == other.id

    def add_tile(self, tile_coord: Tuple[int, int]) -> None:
        if not self.contains_tile(tile_coord):
            self.tile_coords.append(tile_coord)

    def remove_tile(self, tile_coord: Tuple[int, int]) -> None:
        if self.contains_tile(tile_coord):
            self.tile_coords.remove(tile_coord)

    def contains_tile(self, tile_coord: Tuple[int, int]) -> bool:
        return tile_coord in self.tile_coords

    def contains_piece(self, tile_coord: Tuple[int, int]) -> bool:
        return tile_coord in self.pieces.keys()

    def get_piece(self, tile_coord: Tuple[int, int]) -> Piece:
        if self.contains_piece(tile_coord):
            return self.pieces[tile_coord]
        else:
            return None

    def set_piece(self, tile_coord: Tuple[int, int], piece: Piece) -> None:
        self.pieces[tile_coord] = piece

    def remove_piece(self, tile_coord: Tuple[int, int]) -> None:
        if self.contains_piece(tile_coord):
            del self.pieces[tile_coord]


    def get_all_piece_coords(self) -> List[Tuple[int, int]]: #TODO: Fix type signature, actually returns dict_keys
        return self.pieces.keys()

    # TODO: Need to implement this, i.e. set balances etc.
    def initialize_region(self):
        if len(self.tile_coords) > 1:
            hut_coord = self.tile_coords[np.random.choice(range(len(self.tile_coords)))]
            self.set_piece(hut_coord, Hut())

        self.balance = len(self.tile_coords) * RegionConfig.tile_starting_balance

    # TODO: Implement this function properly so it maintains invariances
    def merge_regions(self, other: 'Region'):
        pass

    def check_valid_region(self) -> bool:
        return self.check_tile_same_team() and self.check_tile_connectivity()

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