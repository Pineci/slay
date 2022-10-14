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

    def __init__(self, map: Map=None, tile_coords: List[Tuple[int, int]] = [], initialize: bool=True, id: int=0, team: int=None):
        self.map = map
        self.tile_coords = tile_coords
        self.pieces = {}
        self.id = id
        self.team = team
        
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

    def contains_hut(self) -> bool:
        for tile_coord in self.pieces.keys():
            if self.pieces[tile_coord].name == "hut":
                return True
        return False

    def get_hut_coord(self) -> Tuple[int, int]:
        for tile_coord in self.pieces.keys():
            if self.pieces[tile_coord].name == "hut":
                return tile_coord
        raise Exception("Tried to get hut coordinate, but region did not contain hut!")

    def get_piece(self, tile_coord: Tuple[int, int]) -> Piece:
        if self.contains_piece(tile_coord):
            return self.pieces[tile_coord]
        else:
            return None

    def get_team(self) -> int:
        return self.team

    def get_size(self) -> int:
        return len(self.tile_coords)

    def get_balance(self) -> int:
        return self.balance

    def get_id(self) -> int:
        return self.id

    def set_team(self, team: int) -> None:
        self.team = team

    def set_balance(self, balance: int) -> None:
        self.balance = balance

    def set_piece(self, tile_coord: Tuple[int, int], piece: Piece) -> None:
        self.pieces[tile_coord] = piece

    def remove_piece(self, tile_coord: Tuple[int, int]) -> None:
        if self.contains_piece(tile_coord):
            del self.pieces[tile_coord]

    def get_all_piece_coords(self) -> List[Tuple[int, int]]: #TODO: Fix type signature, actually returns dict_keys
        return self.pieces.keys()

    # TODO: Need to implement this, i.e. set balances etc.
    def initialize_region(self):
        if self.get_size() > 1:
            self.add_hut()
            self.balance = self.get_size() * RegionConfig.tile_starting_balance
        else:
            self.balance = 0

    def add_hut(self):
        if self.get_size() > 1 and not self.contains_hut():
            power_map = {tile_coord: 0 for tile_coord in self.tile_coords}
            for tile_coord in self.pieces.keys():
                power_map[tile_coord] = self.pieces[tile_coord].power
            current_power = 0
            while True:
                current_power_tiles = list(filter(lambda tile_coord: power_map[tile_coord] == current_power, self.tile_coords))
                if len(current_power_tiles) == 0:
                    current_power += 1
                else:
                    inside_tiles = list(filter(lambda tile_coord: all(list(map(lambda neighbor_coord: neighbor_coord in self.tile_coords, self.map.get_tile(tile_coord).get_neighbors_coords()))), current_power_tiles))
                    if len(inside_tiles) > 0:
                        tile_coord = inside_tiles[np.random.randint(len(inside_tiles))]
                        self.set_piece(tile_coord, Hut())
                    else:
                        border_tiles = []
                        for tile_coord in current_power_tiles:
                            if tile_coord not in inside_tiles:
                                border_tiles.append(tile_coord)
                        tile_coord = border_tiles[np.random.randint(len(border_tiles))]
                        self.set_piece(tile_coord, Hut())
                    break
        elif self.get_size() == 1 and self.contains_hut():
            self.remove_piece(self.tile_coords[0])
            self.set_piece(self.tile_coords[0], PalmTree())

    # TODO: Implement this function properly so it maintains invariances
    def eat_region(self, other: 'Region'):
        for tile_coord in other.tile_coords:
            tile = self.map.get_tile(tile_coord)
            tile.set_region_id(self.id)
            self.add_tile(tile_coord)
        for tile_coord in other.pieces.keys():
            if other.get_piece(tile_coord).name != "hut":
                self.set_piece(tile_coord, other.get_piece(tile_coord))
        if other.get_size() > 1:
            self.balance += other.get_balance()

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