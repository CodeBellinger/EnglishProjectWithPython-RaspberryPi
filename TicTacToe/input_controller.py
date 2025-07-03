# input_controller.py
from __future__ import annotations
from typing import TYPE_CHECKING
from direction import Direction

if TYPE_CHECKING:
    from field import Field
    from player import Player

class InputController:
    def __init__(self, grid_size: int = 3):
        self.cursor_position = [0, 0]  # [x, y]
        self.grid_size = grid_size

    def move_cursor(self, direction: str):
        if direction == Direction.LEFT:
            self.cursor_position[0] = (self.cursor_position[0] - 1) % self.grid_size
        elif direction == Direction.RIGHT:
            self.cursor_position[0] = (self.cursor_position[0] + 1) % self.grid_size
        elif direction == Direction.UP:
            self.cursor_position[1] = (self.cursor_position[1] - 1) % self.grid_size
        elif direction == Direction.DOWN:
            self.cursor_position[1] = (self.cursor_position[1] + 1) % self.grid_size

    def get_cursor_position(self) -> tuple:
        return tuple(self.cursor_position)

    def confirm_selection(self, field: Field, player: Player) -> bool:
        x, y = self.get_cursor_position()
        return field.set_tile(x, y, player)