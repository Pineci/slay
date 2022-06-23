from typing import Tuple
from tile import TileType, Tile
from grid import HexGrid, Grid
from config import TILE_ASSET_DIR
import pygame
import json

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

class Render:

    def __init__(self, screen_size: Tuple[int, int]):
        self.screen_size = screen_size
        self.x_margin = 0.1

        self.grid = self.make_grid()

    def initialize_pygame(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)

    def make_grid(self, tile_size: Tuple[int, int], tile_type: TileType) -> Grid:
        tile_rows, tile_cols = tile_size
        if tile_type == TileType.HEXAGON:
            rows, cols = tile_rows+2, 3*tile_cols+2
            scale = HexGrid.scale_from_size(top_left=(0, 0), rows=rows, cols=cols, 
                                            width=self.screen_size[0]-2*self.x_margin)
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
