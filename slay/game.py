from map import Map
from region import Region
from typing import List
import numpy as np

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
        print(len(self.regions))

    def initialize_map(self):
        # Assign tiles to players randomly
        tile_assignments = np.random.randint(self.num_players, size=len(self.map))
        for tile, assignment in zip(self.map, tile_assignments):
            tile.set_team(assignment)

        # Construct regions from map
        regions = []
        for tile in self.map:
            if tile.is_active():
                covered = any(map(lambda r: r.contains_tile(tile.get_tile_coords()), regions))
                if not covered:
                    continuous_tiles = self.map.bfs_find_same_team(tile.get_tile_coords())
                    new_region = Region(map=self.map, tile_coords=continuous_tiles)
                    regions.append(new_region)
        self.regions = regions

    def get_map(self) -> Map:
        return self.map
    