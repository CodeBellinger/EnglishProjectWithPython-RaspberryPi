# game.py
import time
from player import Player
from field import Field
from game_rules import GameRules
from input_controller import InputController
from direction import Direction

class Game:
    def __init__(self):
        self.players = [Player("P1", "X", "255,0,0"), Player("P2", "O", "0,0,255")]
        self.current_player_index = 0
        self.field = Field()
        self.rules = GameRules()
        self.input_controller = InputController()
        self.is_running = False

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def next_turn(self):
        self.switch_player()

    def handle_input(self, key: str):
        if not self.is_running:
            self.start_game()
            return

        if key in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            self.input_controller.move_cursor(key)
            self.field.draw_board_state(self.input_controller.get_cursor_position())

        elif key == Direction.CONFIRM:
            player = self.get_current_player()
            if self.input_controller.confirm_selection(self.field, player):
                if self.rules.check_win(self.field, player):
                    self.end_game(winner=player)
                elif self.rules.check_draw(self.field):
                    self.end_game(winner=None)
                else:
                    self.next_turn()
                    self.field.draw_board_state(self.input_controller.get_cursor_position())

    def start_game(self):
        print("Starting new game.")
        self.is_running = True
        self.field.reset()
        self.current_player_index = 0
        self.input_controller.cursor_position = [0, 0]
        self.field.draw_board_state(self.input_controller.get_cursor_position())

    def end_game(self, winner):
        self.is_running = False
        self.field.draw_board_state(self.input_controller.get_cursor_position())
        time.sleep(0.5)

        if winner:
            print(f"Game over! Winner: {winner.get_name()}")
            winning_tiles = self.rules.get_winning_tiles(self.field)
            winner_color = winner.get_appearance().get_color_as_tuple()
            if winning_tiles:
                self.field.animate_win(winning_tiles, winner_color)
        else:
            print("Game over! It's a draw.")
            self.field.animate_draw()
        
        print("Waiting for input to start a new game...")