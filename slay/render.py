from typing import Tuple
from tile import TileType, Tile
from piece import *
from region import Region
from grid import HexGrid, Grid
from game import Game
from map import Map
from config import *
import pygame
import json
import numpy as np

class TileAsset:

    def __init__(self, file="default.json", asset_json: dict=None, save: bool=False, load: bool=True):
        self.file_path = TILE_ASSET_DIR.joinpath(file)
        self.asset_json = asset_json

        if save:
            self.save_asset(asset_json)
        else:
            self.load_asset()

    def save_asset(self, asset_json: dict) -> None:
        # TODO: Add checker to make sure only valid keys are in the dictionary,
        #       e.g. "team1", "team2", etc.
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(asset_json, f, ensure_ascii=False, indent=4)

    def load_asset(self):
        with open(self.file_path, 'r') as f:
            self.asset_json = json.load(f)
    
    def get_team_color(self, team: int) -> Tuple[int, int, int]:
        key = f"team{team}"
        if key not in self.asset_json.keys():
            raise ValueError(f"No tile asset exists for requested team {team}!")
        else:
            val = self.asset_json[f"team{team}"]
            return tuple(val)

    def get_edge_color(self) -> Tuple[int, int, int]:
        return self.asset_json["edge"]

class TextureAsset:

    def __init__(self, folder="default"):
        self.folder_path = TEXTURE_ASSET_DIR.joinpath(folder)
        self.piece_to_texture = {}
        self.original_texture = {}
        self.scale = DEFAULT_TEXTURE_SCALE # All texture files must be made with scale=15

    def get_piece_texture(self, piece: Piece) -> pygame.Surface:
        name = piece.name
        if name not in self.piece_to_texture:
            surface = pygame.image.load(self.folder_path.joinpath(f'{name}.png'))
            self.original_texture[name] = surface
            self.piece_to_texture[name] = self.make_piece_texture(name)
        return self.piece_to_texture[name]

    def make_piece_texture(self, name: str) -> None:
        surface = self.original_texture[name]
        size = surface.get_size()
        scaling_ratio = self.scale/DEFAULT_TEXTURE_SCALE
        new_size = (size[0]*scaling_ratio, size[1]*scaling_ratio)
        return pygame.transform.scale(surface, new_size)

    def set_scale(self, scale: float) -> None:
        self.scale = scale
        for name in self.piece_to_texture.keys():
            self.piece_to_texture[name] = self.make_piece_texture(name)

class Render:

    def __init__(self, screen_size: Tuple[int, int], game: Game):
        self.screen_size = screen_size
        self.game = game
        self.x_margin = 0.1

        self.grid = self.make_grid()
        self.background_color = (0, 0, 0)

        self.tile_asset = TileAsset()
        self.texture_asset = TextureAsset()

        self.selected_region_id = None

        self.initialize_pygame()

    def initialize_pygame(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

    def make_grid(self) -> Grid:
        tile_rows, tile_cols = self.game.get_map().get_size()
        tile_type = self.game.get_map().get_tile_type()
        if tile_type == TileType.HEXAGON:
            rows, cols = tile_rows+2, 3*tile_cols+2
            scale = HexGrid.scale_from_size(top_left=(0, 0), rows=rows, cols=cols, 
                                            width=self.screen_size[0]*(1-2*self.x_margin))
            width, height = HexGrid.bottom_right_from_scale(top_left=(0, 0), rows=rows, 
                                                            cols=cols, scale=scale)
            top_left = (self.screen_size[0]/2 - width/2, self.screen_size[1]/2 - height/2)
            return HexGrid(rows=rows, cols=cols, top_left=top_left, scale=scale)

    def draw_grid(self, grid_color: Tuple[int, int, int], radius: int=3):
        for row in self.grid.grid:
            for point in row:
                pygame.draw.circle(self.display, grid_color, point, radius, 0)

    def draw_tile(self, tile: Tile, tile_asset: TileAsset, edge_thickness=2) -> None:
        if tile.is_active():
            shape, center = tile.get_shape(self.grid)
            team = tile.get_team()
            pygame.draw.polygon(self.display, tile_asset.get_team_color(team), shape, 0)
            pygame.draw.polygon(self.display, tile_asset.get_edge_color(), shape, edge_thickness)

    def draw_piece(self, tile_coord: Tuple[int, int], piece: Piece, texture_asset: TextureAsset) -> None:
        tile = self.game.get_map().get_tile(tile_coord)
        if tile.is_active():
            shape, center = tile.get_shape(self.grid)
            texture = texture_asset.get_piece_texture(piece)
            texture_size = texture.get_size()
            top_left = (center[0] - texture_size[0]/2, center[1] - texture_size[1] * (0.5 + 0.25))
            self.display.blit(texture, top_left)

    def draw_region_border(self, region: Region) -> None:
        if region.get_id() == self.selected_region_id:
            map_ = self.game.get_map()
            home = region.get_team()
            for tile_coord in region.tile_coords:
                tile = map_.get_tile(tile_coord)
                for neighbor_coord in tile.get_neighbors_coords():
                    if not map_.is_valid_tile_coords(neighbor_coord) or map_.get_tile(neighbor_coord).get_team() != home:
                        edge = tile.get_edge_from_neighbor(neighbor_coord, self.grid)
                        pygame.draw.line(self.display, (255, 255, 255), edge[0], edge[1], 2)

    def draw_region_pieces(self, region: Region) -> None:
        for piece_coord in region.get_all_piece_coords():
            piece = region.get_piece(piece_coord)
            self.draw_piece(piece_coord, piece, self.texture_asset)

    def draw_game(self) -> None:
        for region in self.game.regions.values():
            self.draw_region_border(region)
        for region in self.game.regions.values(): 
            self.draw_region_pieces(region)

    def draw_map(self) -> None:
        for tile in self.game.get_map():
            self.draw_tile(tile, self.tile_asset, edge_thickness=2)

    def find_closest_tile(self, pos: Tuple[int, int]) -> Tile:
        map_ = self.game.get_map()
        sqr_distances = {}
        def get_tile_sqr_distance(tile: Tile):
            tile_coords = tile.get_tile_coords()
            if tile_coords not in sqr_distances.keys():
                shape, center = tile.get_shape(self.grid)
                sqr_distances[tile_coords] = (pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2
            return sqr_distances[tile_coords]
        
        current_tile = map_.get_tile((map_.get_size()[0]//2, map_.get_size()[1]//2))
        done = False
        iter_ = 0
        while not done:
            iter_ += 1
            neighbor_tiles = map(map_.get_tile, filter(map_.is_valid_tile_coords, current_tile.get_neighbors_coords()))
            min_tile = None
            for tile in neighbor_tiles:
                if get_tile_sqr_distance(tile) < get_tile_sqr_distance(current_tile):
                    if not min_tile or get_tile_sqr_distance(tile) < get_tile_sqr_distance(min_tile):
                        min_tile = tile
            if not min_tile:
                done = True
            else:
                current_tile = min_tile
        print(f"Used {iter_} iterations, calculated {len(sqr_distances.keys())} distances")
        return current_tile
        


    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button1, button2, button3, button4, button5 = pygame.mouse.get_pressed(num_buttons=5)
                if button1:
                    row1 = self.grid.grid[0][0:5]
                    row2 = self.grid.grid[1][0:5]
                    row3 = self.grid.grid[2][0:5]

                    rows = row1 + row2 + row3
                    #print(list(map(lambda x: float(f"{(x[0]-72)*20:.2f}"), rows)))
                    #print(list(map(lambda x: float(f"{(x[1]-72)*20:.2f}"), rows)))
                    selected_tile = self.find_closest_tile(pos).get_tile_coords()
                    print(f"SELECTED TILE COORDS {selected_tile}")
                    selected_region = self.game.get_region(selected_tile)
                    if selected_region:
                        self.selected_region_id = selected_region.get_id()
                elif button3:
                    selected_tile = self.find_closest_tile(pos)
                    selected_region = self.game.get_region_by_id(self.selected_region_id)
                    if any(map(selected_region.contains_tile, selected_tile.get_neighbors_coords())):
                        piece = Soldier2()
                        if self.game.check_valid_move(piece, selected_region, selected_tile.get_tile_coords()):
                            self.selected_region_id = self.game.place_piece(piece, selected_region, selected_tile.get_tile_coords())
            elif event.type == pygame.VIDEORESIZE:
                self.screen_size = event.dict['size']
                self.grid = self.make_grid()
                self.texture_asset.set_scale(self.grid.scale)
                pygame.display.update()
            elif event.type == pygame.VIDEOEXPOSE:  # handles window minimising/maximising
                self.screen_size = self.display.get_size()
                self.grid = self.make_grid()
                self.texture_asset.set_scale(self.grid.scale)
                pygame.display.update()

    def main_loop(self):
        while True:
            self.event_handler()
            self.display.fill(self.background_color) 
            self.draw_grid(grid_color=(0, 255, 255), radius=3)
            self.draw_map()
            self.draw_game()
            pygame.display.flip()
        