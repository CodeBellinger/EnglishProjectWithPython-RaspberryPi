# main_connect4.py
# If viergewinnt.py is executed directly from within the 'Project' folder,
# or if 'Project' is added to sys.path, then direct imports are fine.
from . import display_emu # Oder display für Raspberry Pi
import time
from . import remote
import random
import math
import time

# Konstanten
WIDTH = 16
HEIGHT = 16 # Display-Höhe
BOARD_COLS = WIDTH # Spielfeld Spalten
BOARD_ROWS = HEIGHT # Spielfeld Reihen (1 Reihe für fallenden Chip, 15 für Spiel)

PLAYER1_COLOR = (255, 0, 0) # Rot
PLAYER2_COLOR = (0, 0, 255) # Blau
EMPTY_COLOR = (0, 0, 0)   # Schwarz
GRID_COLOR = (50, 50, 50) # Optional: für leere Felder

# Function to get a lighter version of a player's color for the ghost chip
def get_ghost_color(player_color, transparency_factor=0.4):
    """Returns a lighter/more transparent version of a given color."""
    r, g, b = player_color
    return (
        int(r * transparency_factor),
        int(g * transparency_factor),
        int(b * transparency_factor)
    )

# Get the ghost colors once
PLAYER1_GHOST_COLOR = get_ghost_color(PLAYER1_COLOR)
PLAYER2_GHOST_COLOR = get_ghost_color(PLAYER2_COLOR)

FONT_5X5 = {
    'W': [
        "10001",
        "10001",
        "10101",
        "01010",
        "01010"
    ],
    'I': [
        "01110",
        "00100",
        "00100",
        "00100",
        "01110"
    ],
    'N': [
        "10001",
        "11001",
        "10101",
        "10011",
        "10001"
    ],
}

def draw_char(char, start_x, start_y, color):
    """Draws a single character at a given (start_x, start_y) coordinate."""
    if char not in FONT_5X5:
        return # Skip unknown characters

    char_pixels = FONT_5X5[char]
    for r_offset, row_pattern in enumerate(char_pixels):
        for c_offset, pixel_val in enumerate(row_pattern):
            if pixel_val == '1':
                display_emu.set_xy(start_x + c_offset, start_y + r_offset, color)

def animate_winner_text(winner_color, player_number):
    # Text to display
    text = "WIN"
    
    # Calculate starting X position to center the text
    char_width = 5 # Each char is 5 pixels wide
    char_height = 5 # From FONT_5X5

    # Adjust spacing for "WIN" to fit precisely
    # By setting char_spacing to 0, "WIN" will be 3 * 5 = 15 pixels wide.
    # This will allow it to be centered on a 16-pixel display.
    current_char_spacing = 0 

    # Calculate total width of the text with adjusted spacing
    total_text_width = (len(text) * char_width) + \
                       (len(text) - 1) * current_char_spacing
    
    # Calculate starting X position to center the text
    start_text_x = (display_emu.width - total_text_width) // 2
    
    # Ensure start_text_x is not negative (it won't be with "WIN" and 0 spacing)
    if start_text_x < 0:
        start_text_x = 0
    
    # Calculate starting Y position to center the text vertically
    start_text_y = (display_emu.height - char_height) // 2
    if start_text_y < 0:
        start_text_y = 0

    # Animation loop for blinking text
    for _ in range(5): # Blink 5 times (adjust as desired)
        display_emu.fill(EMPTY_COLOR) # Clear screen for this frame

        current_x = start_text_x
        # Iterate over characters in the text string
        for char in text:
            if char.upper() in FONT_5X5:
                draw_char(char.upper(), current_x, start_text_y, winner_color)
            current_x += (char_width + current_char_spacing) # Use the adjusted spacing

        display_emu.show()
        time.sleep(0.8) # Text visible for 0.8 seconds

        display_emu.fill(EMPTY_COLOR) # Clear screen for blink off
        display_emu.show()
        time.sleep(0.3) # Text off for 0.3 seconds

    # Ensure display is cleared after the animation finishes
    display_emu.fill(EMPTY_COLOR)
    display_emu.show()

# Spielfeld-Darstellung
# Global variables for game state (ensure these are correctly defined)
# Spielfeld-Darstellung
#game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
current_player = 1 # 1 or 2
current_column = BOARD_COLS # Current column selected by player
game_over = False
winner = None
falling_chip_row = -1
falling_chip_col = -1
animation_active = False # Flag to control animations

# Helper function to find the next empty row in a column
def get_landing_row(col):
    """
    Finds the last possible row where the chip can land in the given column.
    If the column is full, returns -1.
    """
    for r in range(BOARD_ROWS -1, -1, -1): # Iterate from bottom up
        if game_board[r][col] == EMPTY_COLOR:
            return r
    return -1 # Column is full

def draw_board():
    global game_board, current_column, current_player

    # 1. Clear the entire display or fill with background (optional, but good for clean redraws)
    display_emu.pixels[:, :, :] = EMPTY_COLOR  # Clear the entire display

    # 2. Draw the chip in the first rank
    chip_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
    display_emu.set_xy(current_column, 0, chip_color)  # Display chip in the first rank

    # 3. Draw Ghost Chip
    if not game_over:  # Only show ghost chip if the game is active
        landing_row = get_landing_row(current_column)
        if landing_row != -1:  # If the column is not full
            ghost_color = PLAYER1_GHOST_COLOR if current_player == 1 else PLAYER2_GHOST_COLOR
            display_emu.set_xy(current_column, landing_row, ghost_color)

    # 4. Draw Actual Game Chips (these will overwrite the ghost chip where chips exist)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            color = game_board[r][c]
            if color != EMPTY_COLOR:
                display_emu.set_xy(c, r, color)

    # 4. Update the physical display
    display_emu.show()

def drop_chip(col, player):
    global game_over, winner, chip_falling

    row = get_landing_row(col)
    if row == -1:
        print(f"Column {col} is full!")
        chip_falling = False  # Reset chip_falling if the column is full
        return False # Column is full
    
    # Simulate the chip falling
    for r in range(row + 1):
        game_board[r][col] = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
        draw_board()
        time.sleep(0.1) # Speed of falling animation
        if r < row: # Clear previous falling chip position
            game_board[r][col] = EMPTY_COLOR

    # Place the chip in the final position
    game_board[row][col] = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
    chip_falling = False  # Reset chip_falling after the chip has landed
    draw_board()

def draw_board_without_preview():
    display_emu.fill(EMPTY_COLOR)

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            pixel_color = EMPTY_COLOR
            if game_board[r][c] == 1:
                pixel_color = PLAYER1_COLOR
            elif game_board[r][c] == 2:
                pixel_color = PLAYER2_COLOR
            
            display_y = r
            # OLD: display_emu.set_xy((display_y, c), pixel_color) # This was the (y,x) swap
            # NEW: Back to (x, y) after display_emu refactor
            display_emu.set_xy(c, display_y, pixel_color) 
    display_emu.show()

def animate_fireworks(winner_color):
    display_emu.fill((0, 0, 0)) # Start with a black screen for fireworks
    display_emu.show()
    time.sleep(0.5)

    num_fireworks = 3 # Number of firework bursts
    for _ in range(num_fireworks):
        # Random starting point for the firework (bottom half of the display)
        start_x = random.randint(0, display_emu.width - 1)
        start_y = display_emu.height - 1 # Start from the bottom

        # --- Launch phase ---
        for y in range(start_y, random.randint(3, display_emu.height // 2), -1): # Shoot upwards
            display_emu.fill((0, 0, 0)) # Clear previous frame
            # Draw board might be needed if you want fireworks *over* the board
            # For a pure firework animation, fill black is fine.
            display_emu.set_xy(start_x, y, winner_color)
            display_emu.show()
            time.sleep(0.05)

        # --- Explosion phase ---
        explosion_center_x = start_x
        explosion_center_y = y # Last position before explosion

        # Create random "sparks"
        num_sparks = random.randint(10, 20)
        spark_colors = [winner_color, (255, 255, 0), (255, 165, 0), (255, 255, 255)] # Add some varied colors

        sparks = []
        for _ in range(num_sparks):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.0, 3.0)
            sparks.append({
                'x': float(explosion_center_x),
                'y': float(explosion_center_y),
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle),
                'color': random.choice(spark_colors),
                'life': random.uniform(0.5, 1.5) # How long it lasts
            })

        for t in range(20): # Number of animation frames for explosion
            display_emu.fill((0, 0, 0))
            
            for spark in sparks:
                # Update position
                spark['x'] += spark['vx'] * 0.1
                spark['y'] += spark['vy'] * 0.1
                spark['life'] -= 0.05 # Reduce life

                # Apply gravity (simple)
                spark['vy'] += 0.2

                # Draw spark if alive and within bounds
                if spark['life'] > 0:
                    draw_x = int(round(spark['x']))
                    draw_y = int(round(spark['y']))
                    if 0 <= draw_x < display_emu.width and 0 <= draw_y < display_emu.height:
                        # Fade color based on life
                        r, g, b = spark['color']
                        fade_factor = spark['life'] / (random.uniform(0.5, 1.5))
                        #faded_color = (int(r * fade_factor), int(g * fade_factor), int(b * fade_factor))
                        # Clamp the values to ensure they stay within the 0-255 range
                        faded_r = int(max(0, min(255, r * fade_factor)))
                        faded_g = int(max(0, min(255, g * fade_factor)))
                        faded_b = int(max(0, min(255, b * fade_factor)))
                        faded_color = (faded_r, faded_g, faded_b)
                        display_emu.set_xy(draw_x, draw_y, faded_color)
            
            display_emu.show()
            time.sleep(0.05)

        time.sleep(0.2) # Pause between fireworks bursts

def check_win(game_board, player):
    # Horizontale Überprüfung
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if game_board[r][c] == player and game_board[r][c+1] == player and game_board[r][c+2] == player and game_board[r][c+3] == player:
                return True

    # Vertikale Überprüfung
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if game_board[r][c] == player and game_board[r+1][c] == player and game_board[r+2][c] == player and game_board[r+3][c] == player:
                return True

    # Diagonale (von unten links nach oben rechts)
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS - 3):
            if game_board[r][c] == player and game_board[r+1][c+1] == player and game_board[r+2][c+2] == player and game_board[r+3][c+3] == player:
                return True

    # Diagonale (von oben links nach unten rechts)
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if game_board[r][c] == player and game_board[r-1][c+1] == player and game_board[r-2][c+2] == player and game_board[r-3][c+3] == player:
                return True
    return False

def is_board_full():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if game_board[r][c] == EMPTY_COLOR:  # Check for any empty spot
                return False
    return True

def handle_input(key):
    global current_column, chip_falling, game_over, current_player, game_board, winner # Keep existing globals

    # --- DEBUGGING ---
    print(f"[DEBUG] handle_input called with key: '{key}'")
    print(f"[DEBUG] Before input processing: current_column = {current_column}, chip_falling = {chip_falling}, game_over = {game_over}, current_player = {current_player}")
    # --- END DEBUG PRINTS ---

    if game_over:
        if key == 'ENTER' or key == 'P2_ENTER': # Allow both players to reset
            print("[DEBUG] Game was over, reset initiated.") # Debug print
            reset_game()
        return
    
    if chip_falling: # Ignore input if a chip is currently falling
        print("[DEBUG] Chip is falling, ignoring input.") # Debug print
        return
    
    # Player 1 Controls (A, D, Spacebar)
    if key == 'LEFT':
        old_column = current_column # Save the previous column for debugging
        current_column = max(0, current_column - 1)
        print(f"[DEBUG] Player 1 Moved LEFT: current_column from {old_column} to {current_column}")
    elif key == 'RIGHT':
        # Save the previous column for debugging
        old_column = current_column # Save the previous column for debugging
        current_column = min(BOARD_COLS - 1, current_column + 1)
        print(f"[DEBUG] Player 1 Moved RIGHT: current_column from {old_column} to {current_column}")
    elif key == 'ENTER':
        if current_player == 1:
            print(f"[DEBUG] Player 1 Attempting to drop chip in column {current_column}")
            chip_falling = True
            drop_chip(current_column, current_player)
            chip_falling = False # Reset after drop for next input
            if check_win(game_board, current_player):
                game_over = True
                winner = current_player
                print(f"Player {winner} wins!")
            elif is_board_full():
                game_over = True
                winner = None
                print("It's a draw!")
            else:
                current_player = 3 - current_player # Switch player (1 -> 2, 2 -> 1)
            print(f"[DEBUG] Player 1 After drop: current_player = {current_player}, game_over = {game_over}")

    # Player 2 Controls (Arrow Keys)
    elif key == 'P2_LEFT':
        if current_player == 2: # Ensure only current player's input is processed
            old_column = current_column
            current_column = max(0, current_column - 1)
            print(f"[DEBUG] Player 2 Moved LEFT: current_column from {old_column} to {current_column}")
    elif key == 'P2_RIGHT':
        if current_player == 2:
            old_column = current_column
            current_column = min(BOARD_COLS - 1, current_column + 1)
            print(f"[DEBUG] Player 2 Moved RIGHT: current_column from {old_column} to {current_column}")
    elif key == 'P2_ENTER':
        if current_player == 2:
            print(f"[DEBUG] Player 2 Attempting to drop chip in column {current_column}")
            chip_falling = True
            drop_chip(current_column, current_player)
            chip_falling = False # Reset after drop for next input
            if check_win(game_board, current_player):
                game_over = True
                winner = current_player
                print(f"Player {winner} wins!")
            elif is_board_full():
                game_over = True
                winner = None
                print("It's a draw!")
            else:
                current_player = 3 - current_player # Switch player (1 -> 2, 2 -> 1)
                print(f"[DEBUG] Player 2 After drop: current_player = {current_player}, game_over = {game_over}")
    draw_board() # This is crucial for visual updates
    print("[DEBUG] draw_board() called.")

# --- Utility Functions for Display ---
def draw_pixel(x, y, color):
    # Ensure coordinates are within display boundaries
    if 0 <= x < display_emu.width and 0 <= y < display_emu.height:
        display_emu.set_xy(x, y, color)

def draw_text(x_start, y_start, text, color, font=FONT_5X5):
    current_x = x_start
    for char in text.upper(): # Convert to uppercase to match font keys
        if char in font:
            char_pattern = font[char]
            for r_offset, row_pattern in enumerate(char_pattern):
                for c_offset, pixel_status in enumerate(row_pattern):
                    if pixel_status == '1':
                        draw_pixel(current_x + c_offset, y_start + r_offset, color)
        current_x += len(font[char][0]) + 1 # Move to the next character position (5 width + 1 spacing)

def clear_display():
    display_emu.fill(EMPTY_COLOR)

def reset_game():
    global game_board, current_player, game_over, current_column, winner, chip_falling
    game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)] # Initialize board with EMPTY_COLOR
    current_player = 1
    current_column = BOARD_COLS // 2 # Start in the middle column
    game_over = False
    winner = None
    chip_falling = False  # No chip is falling initially
    setup_remote_bindings() # Call this to set up bindings on game start/reset
    print("[DEBUG] Game reset. Board cleared. Player 1 turn.")
    draw_board() # Draw the cleared board after reset

def game_loop():
    global current_column, chip_falling, game_over, current_player, game_board, winner

    remote.start_listening() # Start the remote listener
    print("--- Running Connect 4 Game Loop ---")
    print("Use a separate terminal to run remote_client.py and send inputs.")
    print("To stop this game loop, interrupt the kernel (Square Stop button above or Kernel -> Interrupt).")

    reset_game() # Initialize the game state and set up bindings

    try:
        while True:
            # Draw the current board state
            draw_board() 
            # A small delay to prevent busy-waiting and allow other threads (like remote listener) to run
            time.sleep(0.05) 
            
            if game_over:
                # Add logic for game over animations, showing winner etc.
                if winner == 1:
                    winner_color = PLAYER1_COLOR
                    print(f"--- Game Over! Winner: Player 1 ---")
                elif winner == 2:
                    winner_color = PLAYER2_COLOR
                    print(f"--- Game Over! Winner: Player 2 ---")
                else:
                    winner_color = EMPTY_COLOR # Or a neutral color for draw
                    print("--- Game Over! It's a draw! ---")

                # You can add calls to animate_fireworks and animate_winner_text here if they exist
                animate_fireworks(winner_color)
                animate_winner_text(winner_color, winner)
                
                # Keep drawing the final board until reset
                draw_board() # Redraw final state
                time.sleep(0.5) # Wait a bit before checking for reset input
                # The handle_input for 'ENTER' (or 'P2_ENTER') when game_over is True will trigger reset_game
                continue # Continue loop to wait for reset input (from handle_input)
                
    except KeyboardInterrupt:
        print("\n--- Game loop interrupted by user. ---")
    finally:
        print("[DEBUG] Game loop ending. Stopping remote listener.")
        remote.stop_listening() # Ensure listener is stopped on exit

# --- New function to set up remote key bindings ---
def setup_remote_bindings():
    # Clear existing bindings to prevent duplicates if this is called multiple times
    remote.bindings = {} # Clear specific key bindings
    remote.all_binds = [] # Clear all_binds if you use it

    # Player 1 bindings
    remote.bind_key('LEFT', lambda key: handle_input('LEFT'))
    remote.bind_key('RIGHT', lambda key: handle_input('RIGHT'))
    remote.bind_key('ENTER', lambda key: handle_input('ENTER'))

    # Player 2 bindings (using distinct P2_ commands for clarity)
    remote.bind_key('P2_LEFT', lambda key: handle_input('P2_LEFT'))
    remote.bind_key('P2_RIGHT', lambda key: handle_input('P2_RIGHT'))
    remote.bind_key('P2_ENTER', lambda key: handle_input('P2_ENTER'))
    print("[DEBUG] Remote bindings set up.")

if __name__ == '__main__':
    game_loop() # Oder rufe deine Hauptfunktion auf, die das Spiel startet