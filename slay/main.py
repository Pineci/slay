import pygame
from typing import Tuple, List
from tile import Hexagon
from grid import HexGrid


def test_grid():
    bg_color = (0, 0, 0)
    fg_color = (0, 255, 255)
    hx_color = (255, 0, 0)

    w, h = 720, 480
    rows, cols = 30, 30
    radius = 3
    top_left = (w * 0.25, h * 0.25)
    side_length = 15

    hex_rows, hex_cols = 15, 8

    pygame.init()
    root = pygame.display.set_mode((w, h))

    hex_grid = HexGrid(rows=rows, cols=cols, top_left=top_left, scale=side_length)

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
                    hexObject = Hexagon((row, col))
                    hexagon, center = hexObject.get_hexagon(hex_grid)
                    pygame.draw.polygon(root, hx_color, hexagon, 0)
                    pygame.draw.polygon(root, bg_color, hexagon, 2)
                    pygame.draw.circle(root, fg_color, center, radius, 0)
            
            pygame.display.flip()


if __name__ == '__main__':
    test_grid()