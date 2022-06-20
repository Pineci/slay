from tile import Tile
from typing import List
from pieces import Piece
from queue import PriorityQueue

class Region:
    '''
    A region is a contiguous part of the playboard, i.e. connected tiles all of the same type
    '''

    def __init__(self, balance: int=0, tiles: List[Tile] = [], pieces: List[Piece] = []):
        self.balance = balance
        self.tiles = tiles
        self.pieces = pieces

        self.coord_to_tile_map = {tile.get_tile_coords(): tile for tile in self.tiles}

    def add_tile(self, tile: 'Tile'):
        if tile not in self.tiles:
            self.tiles.append(tile)
            self.coord_to_tile_map[tile.get_tile_coords()] = tile

    def remove_tile(self, tile: 'Tile'):
        if tile in self.tiles:
            self.tiles.remove(tile)
            del self.coord_to_tile_map[tile.get_tile_coords()]

    # TODO: Implement this function properly so it maintains invariances
    def merge_regions(self, other: 'Region'):
        ...

    def check_valid_region(self) -> bool:
        return self.check_tile_same_team() and self.check_tile_connectivity() and self.check_piece_containment()

    def check_tile_connectivity(self) -> bool:
        if len(self.tiles > 1):
            tile_coords = list(map(lambda tile: tile.get_tile_coords(), self.tiles))
            reached = {coord: False for coord in tile_coords}
            queue = PriorityQueue()
            queue.put((0, self.tiles[0]))
            while queue.not_empty():
                priority, tile = queue.get()
                neighbor_coords = tile.get_neighbors_coords()
                for coord in neighbor_coords:
                    if coord in tile_coords:
                        reached[coord] = True
                        queue.put((priority+1, self.coord_to_tile_map[coord]))
            for coord in tile_coords:
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