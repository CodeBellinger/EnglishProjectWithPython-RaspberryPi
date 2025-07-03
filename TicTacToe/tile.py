# tile.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player

class Tile:
    def __init__(self, position: tuple):
        self.owner: Player | None = None
        self.position = position

    def is_owned(self) -> bool:
        return self.owner is not None

    def get_owner(self) -> Player | None:
        return self.owner

    def set_owner(self, player: Player):
        self.owner = player

    def get_position(self) -> tuple:
        return self.position