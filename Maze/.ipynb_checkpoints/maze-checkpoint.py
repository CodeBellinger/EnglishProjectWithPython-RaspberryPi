# maze.py
# This program generates and displays a unique maze on a 16x16 LED-Box.
# The user controls a dot (player) using arrow keys (via remote_client_maze.py)
# and aims to reach a destination. Upon reaching the destination, it displays
# "WIN" and the time taken.

# Imports for LED-Box interaction and game logic
#import ulib: Provides access to display and remote modules
from ulib import display_emu
from ulib import remote
import time # For timing the game and delays
import random # For maze generation and random placement
import math # Not strictly needed for this maze, but good to include if complex visuals were added

# --- Constants ---
# LED-Box dimensions
WIDTH = 16
HEIGHT = 16

# Colors (RGB tuples)
COLOR_WALL = (50, 50, 50)       # Dark gray for maze walls
COLOR_PATH = (0, 0, 0)          # Black for empty paths
COLOR_PLAYER = (0, 255, 0)      # Green for the player dot
COLOR_START = (0, 0, 255)       # Blue for the starting point
COLOR_DESTINATION = (255, 0, 0) # Red for the destination point
COLOR_TEXT = (255, 255, 255)    # White for "WIN" text and time

# Font definition for 5x5 characters (reused from connect4.py)
# This font is designed for a 5x5 pixel area per character.
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
    '0': [ "01110", "10010", "10110", "11010", "01110" ],
    '1': [ "01000", "11000", "01000", "01000", "11100" ],
    '2': [ "01110", "10010", "01100", "00100", "11110" ],
    '3': [ "11110", "00010", "01110", "00010", "11110" ],
    '4': [ "00100", "01100", "10100", "11110", "00100" ],
    '5': [ "11110", "10000", "11110", "00010", "11110" ],
    '6': [ "01110", "10000", "11110", "10010", "01110" ],
    '7': [ "11110", "00010", "00100", "01000", "10000" ],
    '8': [ "01110", "10010", "01110", "10010", "01110" ],
    '9': [ "01110", "10010", "01110", "00010", "11110" ],
    '.': [ "00000", "00000", "00000", "00000", "01000" ], # Small dot for seconds
    's': [ "01110", "10000", "01110", "00010", "11100" ]
}

# --- Global Game State Variables ---
maze = []               # 2D list to store the maze grid (0 for path, 1 for wall)
player_pos = [0, 0]     # [row, col]
start_pos = [0, 0]      # [row, col]
destination_pos = [0, 0] # [row, col]
game_active = False     # True if game is running, False when won/reset
start_time = 0.0        # To track game duration
game_won_time = 0.0     # Stores the time when the game was won

# --- Maze Generation Functions ---

def create_grid(rows, cols, initial_value):
    """Initializes a 2D grid with a given initial value."""
    return [[initial_value for _ in range(cols)] for _ in range(rows)]

def is_valid(r, c, rows, cols):
    """Checks if a given coordinate is within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def generate_maze_recursive_backtracker(grid_rows, grid_cols):
    """
    Generates a maze using the Recursive Backtracker algorithm.
    The maze is represented by a grid of 0s (paths) and 1s (walls).
    Initializes a grid twice the size for walls, then carves paths.
    """
    global maze

    # The actual maze grid needs to be larger to represent walls between cells.
    # We will work on a grid where cells are (2r+1, 2c+1) and walls are even indices.
    # Final maze will be WIDTH x HEIGHT.
    # Start with all walls, then carve paths.
    # Example: A 2x2 logical maze needs (2*2+1)x(2*2+1) = 5x5 grid.
    # For a 16x16 display, we consider it as 8x8 "cells" where each cell is 2x2 actual pixels,
    # and walls are 1 pixel thick.
    # Let's simplify and make the internal maze generation slightly smaller
    # and then scale it to fit the 16x16 display, ensuring start/end are on paths.

    # Let's generate a maze that is (WIDTH/2) x (HEIGHT/2) cells for simplicity,
    # and then scale it up to the display.
    # This means each cell in the logical maze corresponds to 2x2 pixels on the display,
    # and walls are 1 pixel thick.
    
    # Grid for maze generation logic (e.g., 8x8 cells for a 16x16 display)
    logical_rows = HEIGHT // 2
    logical_cols = WIDTH // 2

    # Initialize all cells as unvisited and all walls as present
    # We use a representation where grid[r][c] is 0 for wall, 1 for path
    # and initially everything is a wall.
    # This will be simpler: 0=path, 1=wall in the final 16x16 grid
    maze = create_grid(HEIGHT, WIDTH, 1) # Initialize all as walls (1)

    # Visited grid for the logical cells
    visited = create_grid(logical_rows, logical_cols, False)

    # Stack for DFS (Depth-First Search)
    stack = []

    # Choose a random starting cell for maze generation
    start_logical_r = random.randrange(logical_rows)
    start_logical_c = random.randrange(logical_cols)

    # Mark the starting logical cell as visited
    visited[start_logical_r][start_logical_c] = True
    stack.append((start_logical_r, start_logical_c))

    # Carve out the starting logical cell on the actual display grid
    maze[start_logical_r * 2 + 1][start_logical_c * 2 + 1] = 0

    while stack:
        current_logical_r, current_logical_c = stack[-1] # Peek at the top cell

        # Define possible neighbors and the wall positions between them
        neighbors = []
        # (dr, dc) for neighbor, (wr, wc) for wall
        possible_moves = [
            ((-1, 0), (-1, 0)), # Up
            ((1, 0), (1, 0)),   # Down
            ((0, -1), (0, -1)), # Left
            ((0, 1), (0, 1))    # Right
        ]

        # Find unvisited neighbors
        for (dr, dc), (wr, wc) in possible_moves:
            next_logical_r, next_logical_c = current_logical_r + dr, current_logical_c + dc
            if is_valid(next_logical_r, next_logical_c, logical_rows, logical_cols) and \
               not visited[next_logical_r][next_logical_c]:
                neighbors.append(((next_logical_r, next_logical_c), (current_logical_r * 2 + 1 + wr, current_logical_c * 2 + 1 + wc)))

        if neighbors:
            # Pick a random unvisited neighbor
            (next_logical_r, next_logical_c), (wall_r, wall_c) = random.choice(neighbors)

            # Carve a path to the chosen neighbor cell
            maze[next_logical_r * 2 + 1][next_logical_c * 2 + 1] = 0
            
            # Carve the wall between current and chosen neighbor
            # The wall is at the mid-point between the center of current cell and next cell.
            # Example: Current (1,1), next (1,3). Wall is at (1,2).
            # This is simpler if we define walls relative to the current cell
            # The wall is *between* the current cell (2r+1, 2c+1) and the next cell (2r_next+1, 2c_next+1)
            # The wall pixel will be at (2r+1+dr, 2c+1+dc)
            maze[current_logical_r * 2 + 1 + dr][current_logical_c * 2 + 1 + dc] = 0

            # Mark the new cell as visited
            visited[next_logical_r][next_logical_c] = True
            stack.append((next_logical_r, next_logical_c))
        else:
            # No unvisited neighbors, backtrack
            stack.pop()
    
    # Ensure a border of walls around the maze (if not already present from initial setup)
    for r in range(HEIGHT):
        maze[r][0] = 1
        maze[r][WIDTH - 1] = 1
    for c in range(WIDTH):
        maze[0][c] = 1
        maze[HEIGHT - 1][c] = 1


def place_start_and_destination():
    """
    Places the start and destination points randomly on paths within the maze.
    Ensures they are not the same pixel.
    """
    global start_pos, destination_pos, player_pos

    # Find all possible path pixels
    path_pixels = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if maze[r][c] == 0: # If it's a path
                path_pixels.append((r, c))

    if not path_pixels:
        raise ValueError("No paths found in the maze, cannot place start/destination.")

    # Choose random start and destination from path pixels
    start_pos = list(random.choice(path_pixels))
    
    # Ensure destination is different from start
    while True:
        destination_pos = list(random.choice(path_pixels))
        if destination_pos != start_pos:
            break
            
    player_pos[0], player_pos[1] = start_pos[0], start_pos[1] # Player starts at start_pos

# --- Drawing Functions ---

def draw_char(char, start_x, start_y, color):
    """Draws a single character at a given (start_x, start_y) coordinate."""
    if char not in FONT_5X5:
        return # Skip unknown characters

    char_pixels = FONT_5X5[char]
    for r_offset, row_pattern in enumerate(char_pixels):
        for c_offset, pixel_val in enumerate(row_pattern):
            if pixel_val == '1':
                # Note: display.set_xy expects (row, col) or (y, x). If using import ulib: ulib.display.set_xy
                # The font patterns are usually (x_offset, y_offset)
                # So (start_y + r_offset, start_x + c_offset) maps (y, x) correctly.
                display_emu.set_xy((start_y + r_offset, start_x + c_offset), color)

def draw_text(x_start, y_start, text, color, font=FONT_5X5):
    """Draws a string of text on the display."""
    current_x = x_start
    char_width = 5 # Each char is 5 pixels wide from FONT_5X5
    char_spacing = 1 # Space between characters

    for char in text.upper(): # Convert to uppercase to match font keys
        if char in font:
            char_pattern = font[char]
            for r_offset, row_pattern in enumerate(char_pattern):
                for c_offset, pixel_status in enumerate(row_pattern):
                    if pixel_status == '1':
                        # display.set_xy takes (y, x)
                        display_emu.set_xy((y_start + r_offset, current_x + c_offset), color)
            current_x += char_width + char_spacing # Move to the next character position
        else:
            current_x += char_width + char_spacing # Still move even if char not found


def draw_maze():
    """Renders the entire maze, player, start, and destination on the LED-Box."""
    display_emu.fill(COLOR_PATH) # Start with a blank canvas (path color)

    for r in range(HEIGHT):
        for c in range(WIDTH):
            if maze[r][c] == 1: # If it's a wall
                display_emu.set_xy((r, c), COLOR_WALL)

    # Draw start and destination points
    display_emu.set_xy(start_pos, COLOR_START)
    display_emu.set_xy(destination_pos, COLOR_DESTINATION)

    # Draw player
    display_emu.set_xy(player_pos, COLOR_PLAYER)

    display_emu.show() # Push changes to the physical display

# --- Game Logic ---

def reset_game():
    """Resets the game state, generates a new maze, and places points."""
    global game_active, start_time, game_won_time

    print("[DEBUG] Resetting game...")
    generate_maze_recursive_backtracker(HEIGHT, WIDTH)
    place_start_and_destination()
    
    game_active = True
    start_time = 0.0 # Reset start time
    game_won_time = 0.0 # Reset won time

    display_emu.fill(COLOR_PATH) # Clear display before drawing new maze
    display_emu.show()
    time.sleep(0.1) # Small delay for clear

    draw_maze()
    print(f"[DEBUG] Game reset. Start: {start_pos}, Destination: {destination_pos}")
    print(f"[DEBUG] Player at: {player_pos}")


def handle_input(key):
    """
    Handles player movement based on remote key presses.
    Checks for walls before moving the player.
    """
    global player_pos, game_active, start_time, game_won_time

    if not game_active and key not in ['ENTER']: # Allow ENTER to reset even if not active
        return # Ignore input if game is over and not a reset command

    new_r, new_c = player_pos[0], player_pos[1]
    moved = False

    if key == 'LEFT':
        new_c -= 1
    elif key == 'RIGHT':
        new_c += 1
    elif key == 'UP':
        new_r -= 1
    elif key == 'DOWN':
        new_r += 1
    elif key == 'ENTER':
        if not game_active: # If game is not active (e.g., after winning)
            reset_game()
            return
        else:
            print("[DEBUG] Enter pressed during active game (ignored for movement).")
            return

    # Check for valid move (within bounds and not a wall)
    if is_valid(new_r, new_c, HEIGHT, WIDTH) and maze[new_r][new_c] == 0: # 0 means path
        player_pos[0], player_pos[1] = new_r, new_c
        moved = True
        if start_time == 0.0: # Start timer on first move
            start_time = time.monotonic()
            print("[DEBUG] Game timer started.")
    elif is_valid(new_r, new_c, HEIGHT, WIDTH) and maze[new_r][new_c] == 1:
        print(f"[DEBUG] Tried to move to a wall at ({new_r}, {new_c}). Blocked.")
    else:
        print(f"[DEBUG] Tried to move out of bounds to ({new_r}, {new_c}). Blocked.")

    if moved:
        draw_maze() # Redraw the maze with the new player position
        print(f"[DEBUG] Player moved to: {player_pos}")
        # Check for win condition after movement
        if player_pos == destination_pos:
            game_active = False
            game_won_time = time.monotonic() - start_time
            print(f"[DEBUG] Player reached destination! Time: {game_won_time:.2f}s")
            display_win_screen(game_won_time)


def display_win_screen(final_time):
    """Displays "WIN" and the elapsed time on the LED-Box."""
    display_emu.fill(COLOR_PATH) # Clear screen
    
    # Display "WIN"
    # Centering "WIN" (3 chars * 5 width + 2 spacing = 17 pixels, slightly wider than 16, so adjust)
    # Let's target horizontal center for a 16 pixel width.
    # 3 chars * 5 pixels/char = 15 pixels. So, 16 - 15 = 1 pixel difference.
    # We can center it roughly at x=0.5, but pixels are integers.
    # Let's say start_x = 0 to make "W" start at column 0.
    draw_text(0, 3, "WIN", COLOR_TEXT) # Row 3 is a good vertical center for 5x5 font

    # Display time (e.g., "12.34s")
    time_str = f"{final_time:.1f}s" # Format to 1 decimal place
    # Max 5 chars for time + 's', e.g., "99.9s", 4.0s
    # Calculate position to center time string roughly
    # Char width 5, spacing 1. So 6 pixels per char + last char.
    # "12.3s" is 5 chars * 6 - 1 = 29. No, this font is compact.
    # Each char is 5 pixels wide. Spacing 1.
    # "99.9s" (5 characters including '.') means 5*5 + 4*1 = 29 pixels (too wide)
    # We need to render it carefully.
    # Let's render time below WIN, maybe slightly offset.
    # If using 5x5 font and 1 pixel spacing:
    # A 4-char string "X.Ys" is 4*5 + 3*1 = 23 pixels wide. Still too wide.
    # Let's reduce spacing for numbers. Or make font smaller if possible (not with this font).

    # For 16x16, let's simplify and just place it after WIN.
    # Or, try to fit max 3 digits + '.s'
    # "9.9s" (4 chars) -> 4*5 = 20 (too wide).
    # "9s" (2 chars) -> 2*5 = 10 pixels wide. This can be centered.

    # Let's adjust draw_text to center for this resolution
    # Calculate width of the specific time string
    text_width_pixels = sum(len(FONT_5X5.get(c.upper(), ['00000'])[0]) for c in time_str) + \
                        (len(time_str) - 1) * 1 # 1 pixel spacing
    if len(time_str) == 1: text_width_pixels = 5 # Edge case for single digit (e.g., "0s")

    # Center horizontally
    text_start_x = (WIDTH - text_width_pixels) // 2
    if text_start_x < 0: text_start_x = 0 # Avoid negative if string too long

    # Display time below "WIN"
    # "WIN" ends around row 3+5 = 8. So put time at row 9 or 10.
    draw_text(text_start_x, 9, time_str, COLOR_TEXT)

    display_emu.show()
    # Game is inactive, will wait for ENTER to reset in game_loop

# --- Remote Input Setup ---

def setup_remote_bindings():
    """Sets up the remote key bindings for player movement."""
    # Clear existing bindings to prevent duplicates
    remote.bindings = {}
    remote.all_binds = []

    # Bind arrow keys to handle_input
    # These key names correspond to what remote_client.py sends
    remote.bind_key('UP', lambda key: handle_input('UP'))
    remote.bind_key('DOWN', lambda key: handle_input('DOWN'))
    remote.bind_key('LEFT', lambda key: handle_input('LEFT'))
    remote.bind_key('RIGHT', lambda key: handle_input('RIGHT'))
    
    # Bind ENTER to reset the game
    remote.bind_key('ENTER', lambda key: handle_input('ENTER'))
    print("[DEBUG] Remote bindings set up.")


# --- Main Game Loop ---

def game_loop():
    """Main loop for the maze game."""
    global game_active

    remote.start_listening() # Start listening for remote commands
    setup_remote_bindings()       # Set up the key bindings

    print("--- Running Maze Game ---")
    print("Connect to the LED-Box WiFi, access http://led-box.bbrouter/ on your browser.")
    print("Upload this 'maze.py' as a program.")
    print("Run 'remote_client.maze.py' on your local computer to send inputs (UP, DOWN, LEFT, RIGHT, ENTER).")
    print("Press 'ENTER' to start/reset the game after winning.")
    print("To stop this game loop, interrupt the kernel.")

    # Initial game setup
    reset_game()

    try:
        while True:
            if game_active:
                # Game is active, just wait for input
                time.sleep(0.1) # Small delay to prevent busy-waiting
            else:
                # Game is won, waiting for ENTER to reset
                time.sleep(0.5) # Wait a bit longer to reduce CPU usage
                # The handle_input for 'ENTER' will trigger reset_game
    except KeyboardInterrupt:
        print("\n--- Game loop interrupted by user. ---")
    finally:
        print("[DEBUG] Game loop ending. Stopping remote listener.")
        remote.stop_listening() # Ensure listener is stopped on exit

# --- Entry Point ---
if __name__ == "__main__":
    game_loop()

