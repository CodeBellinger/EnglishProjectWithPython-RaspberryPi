# field.py
import time
from ulib import display_emu as display
import constants
from tile import Tile

class Field:
    def __init__(self, size: int = 3):
        self.size = size
        self.grid = [[Tile((col, row)) for col in range(size)] for row in range(size)]

    def get_size(self) -> int:
        return self.size

    def get_tile(self, x: int, y: int) -> Tile | None:
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        return None

    def set_tile(self, x: int, y: int, player) -> bool:
        tile = self.get_tile(x, y)
        if tile and not tile.is_owned():
            tile.set_owner(player)
            return True
        return False

    def is_full(self) -> bool:
        return all(t.is_owned() for r in self.grid for t in r)

    def reset(self):
        for row in self.grid:
            for tile in row:
                tile.owner = None

    def _map_grid_to_display(self, x: int, y: int) -> tuple:
        start_x_pixel = constants.GRID_OFFSET_X + x * (constants.CELL_SIZE + constants.GAP_SIZE)
        start_y_pixel = constants.GRID_OFFSET_Y + y * (constants.CELL_SIZE + constants.GAP_SIZE)
        return start_x_pixel, start_y_pixel

    def draw_cell(self, x: int, y: int, color: tuple):
        start_x, start_y = self._map_grid_to_display(x, y)
        for i in range(constants.CELL_SIZE):
            for j in range(constants.CELL_SIZE):
                display.set_xy((start_y + j, start_x + i), color)

    def draw_board_state(self, cursor_pos: tuple):
        display.fill(constants.BACKGROUND_COLOR)
        
        for y in range(self.size):
            for x in range(self.size):
                tile = self.get_tile(x, y)
                color = constants.BACKGROUND_COLOR
                if tile and tile.is_owned():
                    color = tile.get_owner().get_appearance().get_color_as_tuple()
                self.draw_cell(x, y, color)

        grid_pixel_size = self.size * constants.CELL_SIZE + (self.size - 1) * constants.GAP_SIZE
        for i in range(1, self.size):
            line_pos_x = constants.GRID_OFFSET_X + i * constants.CELL_SIZE + (i - 1) * constants.GAP_SIZE
            line_pos_y = constants.GRID_OFFSET_Y + i * constants.CELL_SIZE + (i - 1) * constants.GAP_SIZE
            for k in range(grid_pixel_size):
                display.set_xy((constants.GRID_OFFSET_Y + k, line_pos_x), constants.GRID_COLOR)
                display.set_xy((line_pos_y, constants.GRID_OFFSET_X + k), constants.GRID_COLOR)
        
        sx, sy = self._map_grid_to_display(*cursor_pos)
        for i in range(constants.CELL_SIZE):
            display.set_xy((sy + i, sx), constants.CURSOR_COLOR)
            display.set_xy((sy + i, sx + constants.CELL_SIZE - 1), constants.CURSOR_COLOR)
        for j in range(constants.CELL_SIZE):
            display.set_xy((sy, sx + j), constants.CURSOR_COLOR)
            display.set_xy((sy + constants.CELL_SIZE - 1, sx + j), constants.CURSOR_COLOR)
            
        display.show()

    def animate_win(self, winning_tiles: list[Tile], winner_color: tuple):
        for _ in range(3): # Blink 3 times
            for tile in winning_tiles:
                self.draw_cell(tile.position[0], tile.position[1], constants.BACKGROUND_COLOR)
            display.show()
            time.sleep(0.2)
            for tile in winning_tiles:
                self.draw_cell(tile.position[0], tile.position[1], winner_color)
            display.show()
            time.sleep(0.2)

    def animate_draw(self):
        for _ in range(3):
            display.fill((50, 50, 50))
            display.show()
            time.sleep(0.2)
            display.fill(constants.BACKGROUND_COLOR)
            display.show()
            time.sleep(0.2)