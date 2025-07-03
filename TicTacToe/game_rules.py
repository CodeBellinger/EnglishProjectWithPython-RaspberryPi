# game_rules.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from field import Field, Tile
    from player import Player

class GameRules:
    def check_win(self, field: Field, player: Player) -> bool:
        size = field.get_size()
        for y in range(size):
            if all(field.get_tile(x, y).get_owner() == player for x in range(size)):
                return True
        for x in range(size):
            if all(field.get_tile(x, y).get_owner() == player for y in range(size)):
                return True
        if all(field.get_tile(i, i).get_owner() == player for i in range(size)):
            return True
        if all(field.get_tile(i, size - 1 - i).get_owner() == player for i in range(size)):
            return True
        return False

    def check_draw(self, field: Field) -> bool:
        return field.is_full()

    def get_winning_tiles(self, field: Field) -> list[Tile]:
        size = field.get_size()
        winning_lines = []
        
        for i in range(size):
            winning_lines.append([field.get_tile(j, i) for j in range(size)])
            winning_lines.append([field.get_tile(i, j) for j in range(size)])
        
        winning_lines.append([field.get_tile(i, i) for i in range(size)])
        winning_lines.append([field.get_tile(i, size - 1 - i) for i in range(size)])

        for line in winning_lines:
            if all(t.is_owned() for t in line) and len(set(t.get_owner() for t in line)) == 1:
                return line
        return []