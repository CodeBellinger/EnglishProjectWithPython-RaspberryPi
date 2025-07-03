# player.py
from player_appearance import PlayerAppearance

class Player:
    def __init__(self, name: str, symbol: str, color_str: str):
        self.name = name
        self.symbol = symbol
        self._appearance = PlayerAppearance(color_str, symbol)

    def get_name(self) -> str:
        return self.name
        
    def get_symbol(self) -> str:
        return self.symbol

    def get_appearance(self) -> PlayerAppearance:
        return self._appearance
        
    def set_appearance(self, appearance: PlayerAppearance):
        self._appearance = appearance