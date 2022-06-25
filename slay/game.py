from map import Map
from region import Region
from piece import Piece
from typing import List, Tuple
import numpy as np

def generate_id(previous_ids):
    uuid = np.random.randint(1e10)
    while uuid in previous_ids:
        uuid = np.random.randint(1e10)
    return uuid

class Game:
    '''
    This class runs the games internal logic, i.e. determining valid moves, applying
    rules, changing the map, etc.
    '''

    # TODO: Implement this class
    def __init__(self, map: Map, num_players: int = 1):
        self.map = map
        self.num_players = num_players
        self.initialize_map()

    def initialize_map(self):
        # Assign tiles to players randomly
        tile_assignments = np.random.randint(self.num_players, size=len(self.map))
        for tile, assignment in zip(self.map, tile_assignments):
            tile.set_team(assignment)

        # Construct regions from map
        regions = []
        unique_ids = []
        for tile in self.map:
            if tile.is_active():
                covered = any(map(lambda r: r.contains_tile(tile.get_tile_coords()), regions))
                if not covered:
                    continuous_tiles = self.map.bfs_find_same_team(tile.get_tile_coords())
                    uuid = generate_id(unique_ids)
                    unique_ids.append(uuid)
                    new_region = Region(map=self.map, tile_coords=continuous_tiles, id=uuid)
                    regions.append(new_region)
        self.regions = regions

    def get_map(self) -> Map:
        return self.map

    def get_region(self, tile_coord: Tuple[int, int]) -> Region:
        for region in self.regions:
            if tile_coord in region.tile_coords:
                return region

    #def set_agent(self, team: int, agent: Agent) -> None:
    #    self.agents[team] = agent

    # TODO: Finish this function
    def check_valid_move(self, piece: Piece, original_region: Region, target_coord: Tuple[int, int]) -> bool:
        other_region = self.get_region(target_coord)
        if original_region == other_region:
            if not other_region.contains_piece(target_coord):
                return True
            else:
                other_piece = other_region.get_piece(target_coord)
                if piece.upgradable and other_piece.upgradeable and piece.power + other_piece.power <= Piece.MAX_SOLDIER_LEVEL:
                    return True # Can upgrade the piece
                else:
                    return False
        else:
            # Quick check: See if the other tile contains a more powerful piece
            other_piece = other_region.get_piece(target_coord)
            if other_piece and other_piece.power >= piece.power:
                return False

            # Now need to check to see if there is a surrounding piece which is more powerful
            target_tile = self.get_map().get_tile(target_coord)
            other_pieces = map(lambda coord: other_region.get_piece(coord), target_tile.get_neighbors_coords())
            for other_piece in other_pieces:
                if other_piece.power >= piece.power:
                    return False
            
            return True

    #def place_piece(self, piece: Piece, original_region: Region, target_coord: Tuple[int, int]) -> bool:


    


