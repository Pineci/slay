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
                    uuid = generate_id()
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

    def place_piece(self, piece: Piece, original_region: Region, tile_coord: Tuple[int, int]) -> bool:
        other_region = self.get_region(tile_coord)
        if original_region == other_region:
            pass
        else:
            pass

