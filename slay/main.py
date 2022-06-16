import pygame
from math import sin, cos, pi

class HexGrid:

    def __init__(self, rows, cols, top_left, scale):
        self.rows = rows
        self.cols = cols
        self.top_left = top_left
        self.scale = scale

        self.grid = self.make_hex_grid(top_left=self.top_left, side_length=self.scale)
    
    def make_horizontal_line(self, left_pos=(0, 0), side_length=1):
        return [(left_pos[0] + x*side_length, left_pos[1]) for x in range(self.cols)]

    def make_hex_grid(self,top_left=(0, 0), side_length=1):
        def dx(i):
            if i % 2 == 0:
                return 0
            else:
                return cos(5*pi/3)*side_length
        def dy(i):
            return i*sin(5*pi/3)*side_length
        return [self.make_horizontal_line((top_left[0]+dx(i), top_left[1]-dy(i)), side_length)
            for i in range(self.rows)]

class Hexagon:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def get_hexagon_from_grid(self, hex_grid, top_left=[0, 0], use_grid=True):
        def get(coord):
            if coord[0] < 0 or coord[0] >= hex_grid.cols or coord[1] < 0 or coord[1] >= hex_grid.rows:
                raise Exception
            else:
                return hex_grid.grid[coord[0]][coord[1]]
        if top_left[0] % 2 == 0:
            vertices = [[0, 0], [0, 1], [1, 1], [2, 1], [2, 0], [1, -1]]
        else:
            vertices = [[0, -1], [0, 0], [1, 1], [2, 0], [2, -1], [1, -1]]
        vertices = [[vertex[0] + top_left[0], vertex[1] + top_left[1]] for vertex in vertices]
        center = [top_left[0]+1, top_left[1]]

        if use_grid:
            return list(map(get, vertices)), get(center)
        else:
            return vertices, center

    def get_hex_coords(self):
        return [self.row, 1 + self.col*3 + (self.row % 2) * 2]
    
    def get_hexagon(self, hex_grid):
        return self.get_hexagon_from_grid(hex_grid, self.get_hex_coords(), use_grid=True)

def test_grid():
    bg_color = (0, 0, 0)
    fg_color = (0, 255, 255)
    hx_color = (255, 0, 0)

    w, h = 720, 480
    rows, cols = 30, 30
    radius = 3
    top_left = (w * 0.25, h * 0.25)
    #top_left = (0, 0)
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
                    hexObject = Hexagon(row, col)
                    hexagon, center = hexObject.get_hexagon(hex_grid)
                    pygame.draw.polygon(root, hx_color, hexagon, 0)
                    pygame.draw.polygon(root, bg_color, hexagon, 2)
                    pygame.draw.circle(root, fg_color, center, radius, 0)
            
            pygame.display.flip()


if __name__ == '__main__':
    test_grid()