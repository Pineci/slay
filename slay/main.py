import pygame
from typing import Tuple, List
from tile import Hexagon
from grid import HexGrid
from map import Map
from game import Game
from render import Render

if __name__ == '__main__':
    w, h = 720, 480
    hex_rows, hex_cols = 40, 20
    map = Map(land_points=15, sea_points=10, size=(hex_rows, hex_cols))
    map.make_map()
    game = Game(map, num_players=3)
    renderer = Render((w, h), game)

    renderer.main_loop()