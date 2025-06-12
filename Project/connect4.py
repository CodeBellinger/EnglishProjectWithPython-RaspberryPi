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
BOARD_ROWS = HEIGHT # Spielfeld Reihen

PLAYER1_COLOR = (255, 0, 0) # Rot
PLAYER2_COLOR = (0, 0, 255) # Blau
EMPTY_COLOR = (0, 0, 0)   # Schwarz # Changed from 0 to (0,0,0)
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
                display_emu.set_xy((start_y + c_offset, start_x + r_offset), color)

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
game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)] # Initialized with EMPTY_COLOR (0,0,0)
current_player = 1 # 1 or 2
current_row = BOARD_ROWS - 1  # Start at the bottom row
current_column = BOARD_COLS // 2  # Start in the middle column
game_over = False
winner = None
animation_active = False # Flag to control animations
chip_falling = False # Ensure this is defined globally as well

# Helper function to find the next empty row in a column
def get_landing_row(col):
    """
    Finds the last possible row where the chip can land in the given column.
    If the column is full, returns -1.
    """
    for r in range(BOARD_ROWS -1, -1, -1): # Iterate from bottom up
        if game_board[r][col] == EMPTY_COLOR: # Now comparing with (0,0,0)
            return r
    return -1 # Column is full

def draw_board(blink_state = False):
    global game_over, game_board, current_column, current_player, chip_falling

    # Clear the entire display or fill with background (optional, but good for clean redraws)
    display_emu.fill(EMPTY_COLOR)  # Now correctly clears with (0,0,0)

    # Draw Ghost Chip (with blinking effect)
    if not game_over and not chip_falling:  # Only show ghost chip if the game is active
        landing_row = get_landing_row(current_column)
        if landing_row != -1:  # If the column is not full
            # Only show ghost chip if not blinking or in visible state
            if not blink_state:
                ghost_color = PLAYER1_GHOST_COLOR if current_player == 1 else PLAYER2_GHOST_COLOR
                display_emu.set_xy((landing_row, current_column), ghost_color)

    # Draw Actual Game Chips (game_board now stores colors directly)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            pixel_color = game_board[r][c] # This will be (0,0,0), PLAYER1_COLOR, or PLAYER2_COLOR
            if pixel_color != EMPTY_COLOR: # Only draw if it's not empty
                display_emu.set_xy((r, c), pixel_color)

    # Update the physical display
    display_emu.show()

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
        # Store player's color directly in the board during animation
        game_board[r_anim][col] = chip_color
        draw_board() # Let draw_board handle color conversion
        time.sleep(0.5) # Speed of falling animation
        if r_anim < row: # Clear previous falling chip position
            game_board[r_anim][col] = EMPTY_COLOR # Now clears with (0,0,0)

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

def draw_board_without_preview():
    display_emu.fill(EMPTY_COLOR) # Now correctly fills with (0,0,0)

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            pixel_color = game_board[r][c] # Already the correct color
            display_emu.set_xy((r, c), pixel_color)
    display_emu.show()

def animate_fireworks(winner_color):
    display_emu.fill(EMPTY_COLOR) # Start with a black screen for fireworks (now (0,0,0))
    display_emu.show()
    time.sleep(0.5)

    num_fireworks = 3 # Number of firework bursts
    for _ in range(num_fireworks):
        # Random starting point for the firework (bottom half of the display)
        start_x = random.randint(0, display_emu.width - 1)
        start_y = display_emu.height - 1 # Start from the bottom

        # --- Launch phase ---
        for y in range(start_y, random.randint(3, display_emu.height // 2), -1): # Shoot upwards
            display_emu.fill(EMPTY_COLOR) # Clear previous frame (now (0,0,0))
            display_emu.set_xy((y, start_x), winner_color)
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
            display_emu.fill(EMPTY_COLOR) # Now correctly clears with (0,0,0)
            
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
                        faded_r = int(max(0, min(255, r * fade_factor)))
                        faded_g = int(max(0, min(255, g * fade_factor)))
                        faded_b = int(max(0, min(255, b * fade_factor)))
                        faded_color = (faded_r, faded_g, faded_b)
                        display_emu.set_xy((draw_y, draw_x), faded_color)
            
            display_emu.show()
            time.sleep(0.05)

        time.sleep(0.2) # Pause between fireworks bursts

def check_win(game_board, player):
    # Determine the color of the current player
    player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    # Horizontale Überprüfung
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if game_board[r][c] == player_color and \
               game_board[r][c+1] == player_color and \
               game_board[r][c+2] == player_color and \
               game_board[r][c+3] == player_color:
                return True

    # Vertikale Überprüfung
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if game_board[r][c] == player_color and \
               game_board[r+1][c] == player_color and \
               game_board[r+2][c] == player_color and \
               game_board[r+3][c] == player_color:
                return True

    # Negative Diagonale (von oben links nach unten rechts)
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS - 3):
            if game_board[r][c] == player_color and \
               game_board[r+1][c+1] == player_color and \
               game_board[r+2][c+2] == player_color and \
               game_board[r+3][c+3] == player_color:
                return True

    # Positive Diagonale (von oben rechts nach unten links)
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if game_board[r][c] == player_color and \
               game_board[r-1][c+1] == player_color and \
               game_board[r-2][c+2] == player_color and \
               game_board[r-3][c+3] == player_color:
                return True
    return False

def is_board_full():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if game_board[r][c] == EMPTY_COLOR:  # Check for any empty spot using (0,0,0)
                return False
    return True

def handle_input(key):
    global current_column, current_row, chip_falling, game_over, current_player, game_board, winner # Keep existing globals

    # --- DEBUGGING ---
    print(f"[DEBUG] handle_input called with key: '{key}'")
    print(f"[DEBUG] Before input processing: coordinates = ({current_row},{current_column}), chip_falling = {chip_falling}, game_over = {game_over}, current_player = {current_player}")
    # --- END DEBUG PRINTS ---

    if game_over:
        if key in ['ENTER', 'P2_ENTER']: # Allow both players to reset
            print("[DEBUG] Game was over, reset initiated.") # Debug print
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
        current_column = min(BOARD_COLS - 1, current_column + 1)
        print(f"[DEBUG] Player 1 Moved RIGHT: current_column from {old_column} to {current_column}")
    elif key == 'P2_LEFT' and current_player == 2:
        old_column = current_column
        current_column = max(0, current_column - 1)
        print(f"[DEBUG] Player 2 Moved LEFT: current_column from {old_column} to {current_column}")
    elif key == 'P2_RIGHT' and current_player == 2:
        old_column = current_column
        current_column = min(BOARD_COLS - 1, current_column + 1)
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

# --- Utility Functions for Display ---
def draw_pixel(x, y, color):
    # Ensure coordinates are within display boundaries
    if 0 <= x < display_emu.width and 0 <= y < display_emu.height:
        display_emu.set_xy((y, x), color)

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
    global game_board, current_player, game_over, current_column, current_row, winner, chip_falling

    # Initialize empty board with EMPTY_COLOR (now (0,0,0))
    game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

    current_player = 1 # Player 1 starts
    current_column = BOARD_COLS // 2 # Start in the middle column
    current_row = BOARD_ROWS - 1 # Bottom row
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
        blink_state = False # State for blinking ghost chip
        blink_timer = 0 # For controlling blink speed
        blink_interval = 10 # Adjust as needed (higher = slower blinking)

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
            if game_over:
                # Add logic for game over animations, showing winner etc.
                if winner:
                    winner_color = PLAYER1_COLOR if winner == 1 else PLAYER2_COLOR
                    print(f"--- Game Over! Winner: Player {winner} ---")
                    animate_fireworks(winner_color)
                    animate_winner_text(winner_color, winner)
                else:
                    print("--- Game Over! It's a draw! ---")

                # Keep drawing the final board until reset
                draw_board(False) # Redraw final state without blinking
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