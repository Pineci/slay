from map import Map
from region import Region
from piece import Piece
from typing import List, Tuple, Dict
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
        self.regions: Dict[int, Region] = {}
        for tile in self.map:
            if tile.is_active():
                covered = any(map(lambda r: r.contains_tile(tile.get_tile_coords()), self.regions.values()))
                if not covered:
                    continuous_tiles = self.map.bfs_find_same_team(tile.get_tile_coords())
                    uuid = generate_id(self.regions.keys())
                    self.regions[uuid] = Region(map=self.map, tile_coords=continuous_tiles, id=uuid, team=tile.get_team())
                    for tile_coord in continuous_tiles:
                        self.map.get_tile(tile_coord).set_region_id(uuid)

    def get_map(self) -> Map:
        return self.map

    def get_region(self, tile_coord: Tuple[int, int]) -> Region:
        for region in self.regions.values():
            if region.contains_tile(tile_coord):
                return region

    def get_region_by_id(self, id: int) -> Region:
        return self.regions.get(id)

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
            #TODO: Need to check if target coord is neighbor of current region

            # Quick check: See if the other tile contains a more powerful piece
            other_piece = other_region.get_piece(target_coord)
            if other_piece and other_piece.power >= piece.power:
                return False

            # Now need to check to see if there is a surrounding piece which is more powerful
            target_tile = self.get_map().get_tile(target_coord)
            other_pieces = map(other_region.get_piece, target_tile.get_neighbors_coords())
            for other_piece in other_pieces:
                if other_piece and other_piece.power >= piece.power:
                    return False
            
            return True

    # Already assumes that piece placement is valid
    # Need to check if we connected any regions
    # Need to check if split up any regions
    def place_piece(self, piece: Piece, original_region: Region, target_coord: Tuple[int, int]) -> int:

        # First, edit the tile, regions, and map
        home_team = original_region.get_team()

        # Set the team of the target tile to home team
        target_tile = self.get_map().get_tile(target_coord)
        prev_team = target_tile.get_team()
        target_tile.set_team(home_team)

        # Remove piece and tile from other region, spawn another hut if necessary
        other_region: Region = self.regions[target_tile.get_region_id()]
        other_piece = other_region.get_piece(target_coord)
        other_region.remove_piece(target_coord)
        other_region.remove_tile(target_coord)
        if other_piece and other_piece.name == "hut":
            other_region.set_balance(0)
        if other_region.get_size() == 0:
            del self.regions[other_region.get_id()]
        
        # Add piece to original region
        target_tile.set_region_id(original_region.id)
        self.get_map().set_tile(target_coord, target_tile)
        original_region.add_tile(target_coord)
        original_region.set_piece(target_coord, piece)

        check_regions_for_huts = {other_region.id: other_region}

        neighbor_tiles = list(map(self.get_map().get_tile, list(filter(self.get_map().is_valid_tile_coords, target_tile.get_neighbors_coords()))))
        home_tiles = list(filter(lambda tile: tile.get_team() == home_team, neighbor_tiles))
        away_tiles = list(filter(lambda tile: tile.get_team() == prev_team, neighbor_tiles))
        
        # First go through tiles in the home team
        current_region_id = original_region.get_id()
        for first_idx in range(len(home_tiles)):
            for second_idx in range(first_idx+1, len(home_tiles)):
                first, second = home_tiles[first_idx], home_tiles[second_idx]
                # If both home team tiles are in the same region, they're already connected and we don't need to do anything
                if first.get_region_id() != second.get_region_id():
                    first_region = self.regions[first.get_region_id()]
                    second_region = self.regions[second.get_region_id()]
                    if first_region.get_size() < second_region.get_size():
                        temp = second_region
                        second_region = first_region
                        first_region = temp
                    first_region.eat_region(second_region)
                    second_id = second_region.get_id()
                    del self.regions[second_id]
                    current_region_id = first_region.get_id()
                    

        # Second go through other team tiles and check if we separated a region
        for first_idx in range(len(away_tiles)):
            for second_idx in range(first_idx+1, len(away_tiles)):
                first, second = away_tiles[first_idx], away_tiles[second_idx]
                if first.get_region_id() == second.get_region_id():
                    first_coords, second_coords = first.get_tile_coords(), second.get_tile_coords()
                    # Need to check if there is still a path between first and second
                    if not second_coords in self.get_map().bfs_same_team_generator(first_coords):
                        #TODO: Write a function so split a region in two, and do that right here
                        first_tiles = list(self.get_map().bfs_same_team_generator(first_coords))
                        second_tiles = list(self.get_map().bfs_same_team_generator(second_coords))
                        region = self.regions[first.get_region_id()]

                        hut_coord = region.get_hut_coord()
                        if hut_coord in first_tiles:
                            stay_tiles, remove_tiles = first_tiles, second_tiles
                        else:
                            stay_tiles, remove_tiles = second_tiles, first_tiles
                        
                        uuid = generate_id(self.regions.keys())
                        new_region = Region(self.get_map(), remove_tiles, initialize=False, id=uuid, team=region.get_team())
                        self.regions[uuid] = new_region
                        for tile_coord in remove_tiles:
                            self.get_map().get_tile(tile_coord).set_region_id(uuid)
                            region.remove_tile(tile_coord)
                        for piece_coord in region.pieces.keys():
                            if piece_coord in remove_tiles:
                                new_region.set_piece(piece_coord, region.pieces[piece_coord])
                                del region.pieces[piece_coord]
                        check_regions_for_huts[region.id] = region
                        check_regions_for_huts[new_region.id] = new_region
                        
        for region_id in check_regions_for_huts.keys():
            region = check_regions_for_huts[region_id]
            region.add_hut()


        return current_region_id