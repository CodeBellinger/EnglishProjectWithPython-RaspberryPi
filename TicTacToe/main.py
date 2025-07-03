import time
from ulib import remote
from game import Game

if __name__ == "_main_":
    print("Tic-Tac-Toe Server is running...")
    game = Game()
    remote.bind_all(game.handle_input)
    game.start_game()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")