# from ulib import display_emu as display
from ulib import display
from ulib import remote
import time
import random
import math
import time
import sys

# --- Constants ---
# LED-Box dimensions
WIDTH = 16 # board_cols
HEIGHT = 16 # Display-Höhe, board_rows

# Colors (RGB tuples)
PLAYER1_COLOR = (255, 0, 0) # Rot
PLAYER2_COLOR = (0, 0, 255) # Blau
EMPTY_COLOR = (0, 0, 0)   # Schwarz 
GRID_COLOR = (50, 50, 50) # Weiß (Optional: für leere Felder)

# Font definition for 5x5 characters
# This font is designed for a 5x5 pixel area per character.
FONT_5X5 = {
    'W': ["10001", "10001", "10101", "01010", "01010"],
    'I': ["01110", "00100", "00100", "00100", "01110"],
    'N': ["10001", "11001", "10101", "10011", "10001"],
}

# --- Global Game State Variables ---
game_board = [[EMPTY_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)] # Initialized with EMPTY_COLOR (0,0,0)
current_player = 1 # 1 or 2
current_column = WIDTH // 2  # Start in the middle column
current_row = HEIGHT - 1  # Start at the bottom row
game_over = False
winner = None
animation_active = False # Flag to control animations
chip_falling = False # Ensure this is defined globally as well

# --- Drawing Functions ---

# Coordinate mapping function
def map_coordinates(x, y):
    """
    Maps coordinates to ensure consistency between display and display_emu.
    Adjusts coordinate order based on the module being used.
    """
    if 'ulib.display_emu' in sys.modules:  # Check if we're using display_emu
        return x, y  # No adjustment needed for display_emu
    else:
        return y, x  # Flip the coordinates for the real LED box/display module

def draw_char(char, start_x, start_y, color):
    """Draws a single character at a given (start_x, start_y) coordinate."""
    if char not in FONT_5X5:
        return # Skip unknown characters

    char_pixels = FONT_5X5[char]
    for r_offset, row_pattern in enumerate(char_pixels):
        for c_offset, pixel_val in enumerate(row_pattern):
            if pixel_val == '1':
                unified_start_y, unified_start_x = map_coordinates(start_y + c_offset, start_x + r_offset)
                display.set_xy((unified_start_y, unified_start_x), color)

def draw_board(blink_state = False):
    global game_over, game_board, current_column, current_player, chip_falling

    # Clear the entire display or fill with background (optional, but good for clean redraws)
    display.fill(EMPTY_COLOR)  # Now correctly clears with (0,0,0)

    # Draw Ghost Chip (with blinking effect)
    if not game_over and not chip_falling:  # Only show ghost chip if the game is active
        landing_row = get_landing_row(current_column)
        if landing_row != -1:  # If the column is not full
            # Only show ghost chip if not blinking or in visible state
            if not blink_state:
                unified_landing_row, unified_current_col = map_coordinates(landing_row, current_column)
                chip_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
                display.set_xy((unified_landing_row, unified_current_col), chip_color)

    # Draw Actual Game Chips (game_board now stores colors directly)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            pixel_color = game_board[r][c] # This will be (0,0,0), PLAYER1_COLOR, or PLAYER2_COLOR
            if pixel_color != EMPTY_COLOR: # Only draw if it's not empty
                unified_r, unified_c = map_coordinates(r, c)
                display.set_xy((unified_r, unified_c), pixel_color)

    # Update the physical display with dim
    display.fade(0.5, 0.5, 0.5)

def draw_pixel(x, y, color):
    # Ensure coordinates are within display boundaries
    if 0 <= x < display.width and 0 <= y < display.height:
        unified_y, unified_x = map_coordinates(y,x)
        display.set_xy((unified_y, unified_x), color)

# --- Winning Animation Functions ---

def animate_winner_text(winner_color, player_number):
    # Text to display
    text = "WIN"
    
    # Calculate starting X position to center the text
    char_width = 5 # Each char is 5 pixels wide
    char_height = 5 # From FONT_5X5

    # By setting char_spacing to 0, "WIN" will be 3 * 5 = 15 pixels wide.
    current_char_spacing = 0 

    # Calculate total width of the text with adjusted spacing
    total_text_width = (len(text) * char_width) + \
                       (len(text) - 1) * current_char_spacing
    
    # Calculate starting X position to center the text
    start_text_x = (display.width - total_text_width) // 2
    
    # Ensure start_text_x is not negative (it won't be with "WIN" and 0 spacing)
    if start_text_x < 0:
        start_text_x = 0
    
    # Calculate starting Y position to center the text vertically
    start_text_y = (display.height - char_height) // 2
    if start_text_y < 0:
        start_text_y = 0

    # Animation loop for blinking text
    for _ in range(5): # Blink 5 times (adjust as desired)
        display.fill(EMPTY_COLOR) # Clear screen for this frame
        current_x = start_text_x
        # Iterate over characters in the text string
        for char in text:
            if char.upper() in FONT_5X5:
                # Draw each character row by row
                char_pixels = FONT_5X5[char.upper()]
                for r_offset, row_pattern in enumerate(char_pixels):
                    for c_offset, pixel_val in enumerate(row_pattern):
                        if pixel_val == '1':
                            # Calculate the correct display coordinates
                            unified_x, unified_y = map_coordinates(current_x + c_offset, start_text_y + r_offset)
                            display.set_xy((unified_y, unified_x), winner_color)  # Correctly mapped coordinates
            current_x += (char_width + current_char_spacing)  # Move to the next character position

        display.fade(0.5, 0.5, 0.5)
        time.sleep(0.8) # Text visible for 0.8 seconds

        display.fill(EMPTY_COLOR) # Clear screen for blink off
        time.sleep(0.3) # Text off for 0.3 seconds

    # Ensure display is cleared after the animation finishes
    display.fill(EMPTY_COLOR)

def animate_fireworks(winner_color):
    global animation_active
    
    # Set animation active flag
    animation_active = True

    display.fill(EMPTY_COLOR) # Start with a black screen for fireworks (now (0,0,0))
    time.sleep(0.5)

    num_fireworks = 3 # Number of firework bursts
    for _ in range(num_fireworks):
        # Random starting point for the firework (bottom half of the display)
        start_x = random.randint(0, display.width - 1)
        start_y = display.height - 1 # Start from the bottom

        # --- Launch phase ---
        for y in range(start_y, random.randint(3, display.height // 2), -1): # Shoot upwards
            display.fill(EMPTY_COLOR) # Clear previous frame (now (0,0,0))
            unified_y, unified_start_x = map_coordinates(y, start_x)
            display.set_xy((unified_y, unified_start_x), winner_color)
            display.fade(0.5, 0.5, 0.5)
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
            display.fill(EMPTY_COLOR) # Now correctly clears with (0,0,0)
            
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
                    if 0 <= draw_x < display.width and 0 <= draw_y < display.height:
                        # Fade color based on life
                        r, g, b = spark['color']
                        fade_factor = spark['life'] / (random.uniform(0.5, 1.5))
                        faded_r = int(max(0, min(255, r * fade_factor)))
                        faded_g = int(max(0, min(255, g * fade_factor)))
                        faded_b = int(max(0, min(255, b * fade_factor)))
                        faded_color = (faded_r, faded_g, faded_b)
                        unified_draw_y, unified_draw_x = map_coordinates(draw_y, draw_x)
                        display.set_xy((unified_draw_y, unified_draw_x), faded_color)
            display.fade(0.5, 0.5, 0.5)
            time.sleep(0.05)

        time.sleep(0.2) # Pause between fireworks bursts

    # Reset animation active flag
    animation_active = False

def draw_text(x_start, y_start, text, color, font=FONT_5X5):
    current_x = x_start
    for char in text.upper(): # Convert to uppercase to match font keys
        if char in font:
            char_pattern = font[char]
            for r_offset, row_pattern in enumerate(char_pattern):
                for c_offset, pixel_status in enumerate(row_pattern):
                    if pixel_status == '1':
                        unified_current_x, unified_y_start = map_coordinates(current_x + c_offset, y_start + r_offset)
                        draw_pixel(unified_current_x, unified_y_start, color)
        current_x += len(font[char][0]) + 1 # Move to the next character position (5 width + 1 spacing)

def clear_display():
    display.fill(EMPTY_COLOR)

# --- Connect4 Generation Functions ---
# Helper function to find the next empty row in a column
def get_landing_row(col):
    """
    Finds the last possible row where the chip can land in the given column.
    If the column is full, returns -1.
    """
    for r in range(HEIGHT -1, -1, -1): # Iterate from bottom up
        if game_board[r][col] == EMPTY_COLOR: # Now comparing with (0,0,0)
            return r
    return -1 # Column is full

def drop_chip(col, player):
    global game_over, winner, chip_falling, current_player, game_board

    row = get_landing_row(col)
    if row == -1:
        print(f"Column {col} is full!")
        chip_falling = False  # Reset chip_falling if the column is full
        return False # Column is full
    
    # Determine the color of the chip to drop
    chip_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    # Simulate the chip falling
    for r_anim in range(row + 1):
        draw_board() # Let draw_board handle color conversion
        unified_r_anim, unified_col = map_coordinates(r_anim, col)
        display.set_xy((unified_r_anim, unified_col), chip_color)
        time.sleep(0.05) # Speed of falling animation

    # Place the chip in the final position
    game_board[row][col] = chip_color
    chip_falling = False  # Reset chip_falling after the chip has landed
    draw_board()

    # Check for win or draw
    if check_win(game_board, player): # check_win now handles color comparison
        game_over = True
        winner = player
        print(f"Player {winner} wins!")
    elif is_board_full(): # is_board_full now handles color comparison
        game_over = True
        winner = None
        print("It's a draw!")
    else:
        # Switch turns
        current_player = 3 - current_player  # Switch player (1 -> 2, 2 -> 1)
        print(f"[DEBUG] Turn switched. Current player: {current_player}")

    return True

def check_win(game_board, player):
    # Determine the color of the current player
    player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    # Horizontale Überprüfung
    for r in range(HEIGHT):
        for c in range(WIDTH - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r, unified_c2 = map_coordinates(r, c + 1)
            unified_r, unified_c3 = map_coordinates(r, c + 2)
            unified_r, unified_c4 = map_coordinates(r, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r][unified_c2] == player_color and \
               game_board[unified_r][unified_c3] == player_color and \
               game_board[unified_r][unified_c4] == player_color:
                return True

    # Vertikale Überprüfung
    for c in range(WIDTH):
        for r in range(HEIGHT - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r2, unified_c = map_coordinates(r + 1, c)
            unified_r3, unified_c = map_coordinates(r + 2, c)
            unified_r4, unified_c = map_coordinates(r + 3, c)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r2][unified_c] == player_color and \
               game_board[unified_r3][unified_c] == player_color and \
               game_board[unified_r4][unified_c] == player_color:
                return True

    # Negative Diagonale (von oben links nach unten rechts)
    for r in range(HEIGHT - 3):
        for c in range(WIDTH - 3):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r2, unified_c2 = map_coordinates(r + 1, c + 1)
            unified_r3, unified_c3 = map_coordinates(r + 2, c + 2)
            unified_r4, unified_c4 = map_coordinates(r + 3, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r2][unified_c2] == player_color and \
               game_board[unified_r3][unified_c3] == player_color and \
               game_board[unified_r4][unified_c4] == player_color:
                return True

    # Positive Diagonale (von oben rechts nach unten links)
    for c in range(WIDTH - 3):
        for r in range(3, HEIGHT):
            unified_r, unified_c = map_coordinates(r, c)
            unified_r5, unified_c2 = map_coordinates(r - 1, c + 1)
            unified_r6, unified_c3 = map_coordinates(r - 2, c + 2)
            unified_r7, unified_c4 = map_coordinates(r - 3, c + 3)
            if game_board[unified_r][unified_c] == player_color and \
               game_board[unified_r5][unified_c2] == player_color and \
               game_board[unified_r6][unified_c3] == player_color and \
               game_board[unified_r7][unified_c4] == player_color:
                return True
    return False

def is_board_full():
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if game_board[r][c] == EMPTY_COLOR:  # Check for any empty spot using (0,0,0)
                return False
    return True

# --- Game Logic ---

def reset_game():
    """Resets the game state, draws a new board, and displays a player's chip."""
    global game_board, current_player, game_over, current_column, current_row, winner, chip_falling, animation_active, animations_completed

    # Reset all necessary flags
    game_board = [[EMPTY_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    current_player = 1
    current_column = WIDTH // 2
    current_row = HEIGHT - 1
    game_over = False
    winner = None
    chip_falling = False
    animation_active = False
    animations_completed = False  # Reset animations completed flag

    setup_remote_bindings() # Call this to set up bindings on game start/reset
    print("[DEBUG] Game reset. Board cleared. Player 1 turn.")
    draw_board() # Draw the cleared board after reset

def handle_input(key):
    global current_column, current_row, chip_falling, game_over, current_player, game_board, winner, animation_active # Keep existing globals

    # --- DEBUGGING ---
    print(f"[DEBUG] handle_input called with key: '{key}'")
    print(f"[DEBUG] Before input processing: coordinates = ({current_row},{current_column}), chip_falling = {chip_falling}, game_over = {game_over}, current_player = {current_player}")
    # --- END DEBUG PRINTS ---

    if game_over:
        if key in ['ENTER', 'P2_ENTER']: # Allow both players to reset
            print("[DEBUG] Game was over, reset initiated.") # Debug print
            if animation_active:
                print("[DEBUG] Animation is active, waiting for it to finish.")
                return  # Do not reset while animation is active
            reset_game()
        return
    
    if chip_falling: # Ignore input if a chip is currently falling
        print("[DEBUG] Chip is falling, ignoring input.") # Debug print
        return
    
    # Restrict input to the current player
    if current_player == 1 and key not in ['LEFT', 'RIGHT', 'ENTER']:
        print("[DEBUG] Ignoring input: Not Player 1's turn.")
        return
    elif current_player == 2 and key not in ['P2_LEFT', 'P2_RIGHT', 'P2_ENTER']:
        print("[DEBUG] Ignoring input: Not Player 2's turn.")
        return

    # Handle movement - using elif to ensure only one block executes
    if key == 'LEFT' and current_player == 1:
        old_column = current_column
        current_column = max(0, current_column - 1)
        print(f"[DEBUG] Player 1 Moved LEFT: current_column from {old_column} to {current_column}")
    elif key == 'RIGHT' and current_player == 1:
        old_column = current_column
        current_column = min(WIDTH - 1, current_column + 1)
        print(f"[DEBUG] Player 1 Moved RIGHT: current_column from {old_column} to {current_column}")
    elif key == 'P2_LEFT' and current_player == 2:
        old_column = current_column
        current_column = max(0, current_column - 1)
        print(f"[DEBUG] Player 2 Moved LEFT: current_column from {old_column} to {current_column}")
    elif key == 'P2_RIGHT' and current_player == 2:
        old_column = current_column
        current_column = min(WIDTH - 1, current_column + 1)
        print(f"[DEBUG] Player 2 Moved RIGHT: current_column from {old_column} to {current_column}")
    elif key in ['ENTER', 'P2_ENTER']:
        print(f"[DEBUG] Player {current_player} Attempting to drop chip in column {current_column}")

        # Set chip_falling to True before animation starts
        chip_falling = True
        
        # Let drop_chip handle the animation and placement
        successful_drop = drop_chip(current_column, current_player)
        if not successful_drop:
            return  # Column was full, drop_chip already handled it
        
    # Draw board after movement (even if chip wasn't dropped)
    if key in ['LEFT', 'RIGHT', 'P2_LEFT', 'P2_RIGHT']:
        draw_board()
    
    print(f"[DEBUG] After input processing: coordinates = ({current_row},{current_column}), chip_falling = {chip_falling}, game_over = {game_over}, current_player = {current_player}")


# --- Remote Input Setup ---

def setup_remote_bindings():
    """Sets up the remote key bindings for player movement."""
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

# --- Main Game Loop ---

def game_loop():
    """Main loop for the maze game."""
    global current_column, chip_falling, game_over, current_player, game_board, winner, animation_active

    remote.start_listening() # Start the remote listener
    setup_remote_bindings()  # Set up the key bindings

    print("--- Running Connect 4 Game Loop ---")
    print("Use a separate terminal to run remote_client.py and send inputs.")
    print("To stop this game loop, interrupt the kernel (Square Stop button above or Kernel -> Interrupt).")

    # Initial game setup
    reset_game() # Initialize the game state and set up bindings

    # Add a flag to track if animations have completed
    animations_completed = False

    try:
        blink_state = False # State for blinking ghost chip
        blink_timer = 0 # For controlling blink speed
        blink_interval = 5 # Adjust as needed (higher = slower blinking)

        while True:
            # Toggle blink state based on timer
            blink_timer += 1
            if blink_timer >= blink_interval:
                blink_state = not blink_state
                blink_timer = 0

                # Draw board with current blink state
                draw_board(blink_state) # Pass the blinking_state here!

            # For smoother blinking, use a shorter sleep time
            time.sleep(0.05)
            
            # Handle game_over states
            if game_over and not animations_completed:
                # Add logic for game over animations, showing winner etc.
                if winner:
                    winner_color = PLAYER1_COLOR if winner == 1 else PLAYER2_COLOR
                    print(f"--- Game Over! Winner: Player {winner} ---")
                    animate_fireworks(winner_color)
                    animate_winner_text(winner_color, winner)
                else:
                    print("--- Game Over! It's a draw! ---")
                
                # Mark animations as completed
                animations_completed = True

                # Keep drawing the final board until reset
                draw_board(False) # Redraw final state without blinking
                time.sleep(0.5) # Wait a bit before checking for reset input
                # The handle_input for 'ENTER' (or 'P2_ENTER') when game_over is True will trigger reset_game
                continue # Continue loop to wait for reset input (from handle_input)
                
            # If animations are completed, wait for reset
            if animations_completed and game_over:
                time.sleep(0.5)  # Avoid busy looping
                continue

    except KeyboardInterrupt:
        print("\n--- Game loop interrupted by user. ---")
    finally:
        print("[DEBUG] Game loop ending. Stopping remote listener.")
        remote.stop_listening() # Ensure listener is stopped on exit

if __name__ == "__main__":
    if 'display_emu' in sys.modules and not hasattr(display, 'pixels'):
        print("[DEBUG] Initializing display_emu pixels for notebook environment.")
        try:
            import numpy as np # Ensure numpy is imported if display_emu needs it
            display.pixels = np.zeros((display.height, display.width, 3), dtype=np.uint8)
        except ImportError:
            print("[ERROR] NumPy not found. Emulator display will not work correctly.")
            print("Please ensure your ulib/display_emu.py (emulator) is correctly configured with numpy.")
            display.pixels = [[(0,0,0) for _ in range(display.width)] for _ in range(display.height)]

    game_loop() # Start the game loop