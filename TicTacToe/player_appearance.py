# player_appearance.py
class PlayerAppearance:
    def __init__(self, color: str, icon: str):
        self.color = color
        self.icon = icon

    def get_color(self) -> str:
        return self.color

    def set_color(self, color: str):
        self.color = color
        
    def get_icon(self) -> str:
        return self.icon
        
    def set_icon(self, icon: str):
        self.icon = icon

    def get_color_as_tuple(self) -> tuple:
        parts = self.color.split(',')
        return int(parts[0]), int(parts[1]), int(parts[2])