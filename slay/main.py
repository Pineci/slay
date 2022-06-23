import pygame
from typing import Tuple, List
from tile import Hexagon
from grid import HexGrid
from map import Map


def test_grid():
    bg_color = (0, 0, 0)
    fg_color = (0, 255, 255)
    hx_color = (255, 0, 0)
    db_color = (255, 255, 0)

    w, h = 720, 480
    radius = 3
    top_left = (w * 0.1, h * 0.1)
    side_length = 10

    hex_rows, hex_cols = 41, 20
    rows, cols = hex_rows+2, 3*hex_cols + 2

    pygame.init()
    root = pygame.display.set_mode((w, h))

    hex_grid = HexGrid(rows=rows, cols=cols, top_left=top_left, scale=side_length)
    test_map = Map(land_points=15, sea_points=10, size=(hex_rows, hex_cols))
    test_map.make_map()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

            root.fill(bg_color)
            for row in hex_grid.grid:
                for point in row:
                    pygame.draw.circle(root, fg_color, point, radius, 0)
            for row in range(hex_rows):
                for col in range(hex_cols):
                    hexObject = test_map.get_tile((row, col))
                    #if hexObject.is_active():
                    edge_color = bg_color
                    if hexObject.priority == 0:
                            edge_color = (255, 255, 255)
                    if hexObject.is_active():
                        color = (255, min(60*hexObject.priority, 255), 0)
                    else:
                        color = (0, min(60*hexObject.priority, 255), 255)
                    hexagon, center = hexObject.get_shape(hex_grid)
                    pygame.draw.polygon(root, color, hexagon, 0)
                    pygame.draw.polygon(root, edge_color, hexagon, 2)
                    #pygame.draw.circle(root, fg_color, center, radius, 0)
                    i,j = hexObject.get_grid_coords()
                    top_left = hex_grid.grid[i][j]
                    #pygame.draw.circle(root, db_color, top_left, radius, 0)
            '''
            for row in range(hex_rows):
                for col in range(hex_cols):
                    hexObject = Hexagon((row, col))
                    hexagon, center = hexObject.get_hexagon(hex_grid)
                    pygame.draw.polygon(root, hx_color, hexagon, 0)
                    pygame.draw.polygon(root, bg_color, hexagon, 2)
                    #pygame.draw.circle(root, fg_color, center, radius, 0)
                    i,j = hexObject.get_grid_coords()
                    top_left = hex_grid.grid[i][j]
                    #pygame.draw.circle(root, db_color, top_left, radius, 0)
            '''
            pygame.display.flip()


if __name__ == '__main__':
    test_grid()