# maze.py
# This program generates and displays a unique maze on a 16x16 LED-Box.
# The user controls a dot (player) using arrow keys (via remote_client_maze.py)
# and aims to reach a destination. Upon reaching the destination, it displays
# "WIN" and the time taken.

# Imports for LED-Box interaction and game logic
#import ulib: Provides access to display and remote modules
from ulib import display_emu as display
from ulib import remote
import time # For timing the game and delays
import random # For maze generation and random placement
import sys
import math # Not strictly needed for this maze, but good to include if complex visuals were added
from collections import deque # Needed for the longest path (BFS) algorithm

# --- Constants ---
# LED-Box dimensions
WIDTH = 16
HEIGHT = 16

# Colors (RGB tuples)
COLOR_WALL = (0, 0, 0)          # Black for maze walls
COLOR_PATH = (255, 255, 255)    # White for empty path
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

def is_valid(r, c, logical_rows, logical_cols):
    """Checks if a given coordinate is within the grid boundaries."""
    return 0 <= r < logical_rows and 0 <= c < logical_cols

def generate_maze_recursive_backtracker():
    """
    Generates a maze using the Recursive Backtracker algorithm.
    The maze is represented by a grid of 0s (paths) and 1s (walls).
    Initializes a grid twice the size for walls, then carves paths.
    """
    global maze

    # Initialize the entire physical maze grid to all walls (1)
    maze = create_grid(HEIGHT, WIDTH, 1)

    # Grid for maze generation logic (e.g., 8x8 cells for a 16x16 display)
    logical_rows = (HEIGHT - 1) // 2
    logical_cols = (WIDTH - 1) // 2

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
        # Define logical moves (dr, dc) for neighbor
        possible_moves = [
            (-1, 0), # Up
            (1, 0),  # Down
            (0, -1), # Left
            (0, 1)  # Right
        ]

        # Find unvisited neighbors
        for dr, dc in possible_moves:
            next_logical_r, next_logical_c = current_logical_r + dr, current_logical_c + dc
            # Ensure wall is actually a wall before carving
            if (is_valid(next_logical_r, next_logical_c, logical_rows, logical_cols) and
               not visited[next_logical_r][next_logical_c]):
                # Store logical next and original dr,dc
                neighbors.append((next_logical_r, next_logical_c, dr, dc))

        if neighbors:
            # Pick a random unvisited neighbor
            (next_logical_r, next_logical_c, dr, dc) = random.choice(neighbors)
            # Carve a path to the chosen neighbor cell (physical coord)
            maze[next_logical_r * 2 + 1][next_logical_c * 2 + 1] = 0
            wall_r = current_logical_r * 2 + 1 + dr
            wall_c = current_logical_c * 2 + 1 + dc
            maze[wall_r][wall_c] = 0
            
            # Mark the new cell as visited and add to stack
            visited[next_logical_r][next_logical_c] = True
            stack.append((next_logical_r, next_logical_c))
        else:
            # No unvisited neighbors, backtrack
            stack.pop()

    print("[DEBUG] Maze generated.")
    
def find_farthest_path_pixel(start_node):
    """
    Performs a Breadth-First Search (BFS) starting from a given node
    to find the pixel on the path that is farthest away.
    Returns the coordinates of the farthest pixel.
    """
    q = deque([(start_node, 0)]) # Queue stores (node, distance)
    visited = {start_node}
    farthest_node = start_node
    max_dist = 0

    while q:
        (r, c), dist = q.popleft()

        if dist > max_dist:
            max_dist = dist
            farthest_node = (r, c)

        # Check neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is a valid path pixel and not visited
            if (is_valid_physical_cell(nr, nc) and
                maze[nr][nc] == 0 and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                q.append(((nr, nc), dist + 1))

    return farthest_node

def find_dead_ends():
    """Returns a list of all dead-end path pixels (with only one path neighbor)."""
    dead_ends = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if maze[r][c] == 0:
                neighbors = 0
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < HEIGHT and 0 <= nc < WIDTH and maze[nr][nc] == 0:
                        neighbors += 1
                if neighbors == 1:
                    dead_ends.append((r, c))
    return dead_ends

def place_start_and_destination():
    """
    Places start and destination at the two dead ends with the longest path between them.
    """
    global start_pos, destination_pos, player_pos

    dead_ends = find_dead_ends()
    if len(dead_ends) < 2:
        raise ValueError("Not enough dead ends to place start and destination.")
    
    # Find the pair of dead ends with the longest path between them
    max_dist = -1
    best_pair = (dead_ends[0], dead_ends[1])

    for i in range(len(dead_ends)):
        for j in range(i+1, len(dead_ends)):
            a, b = dead_ends[i], dead_ends[j]
            dist = path_distance(a, b)
            if dist > max_dist:
                max_dist = dist
                best_pair = (a, b)

    start_pos = list(best_pair[0])
    destination_pos = list(best_pair[1])
    player_pos[0], player_pos[1] = start_pos[0], start_pos[1]
    print(f"[DEBUG] Start at dead end: {start_pos}, Destination at dead end: {destination_pos}, Distance: {max_dist}")

def path_distance(a, b):
    """Returns the number of steps in the shortest path between a and b in the maze."""
    from collections import deque
    visited = set()
    queue = deque([(a, 0)])
    visited.add(a)
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == b:
            return dist
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < HEIGHT and 0 <= nc < WIDTH and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist+1))
    return -1 # Not connected (should not happen in a perfect maze)

# --- Drawing Functions ---

def draw_char(char, start_x, start_y, color):
    """Draws a single character at a given (start_x, start_y) coordinate."""
    if char not in FONT_5X5:
        return # Skip unknown characters

    char_pixels = FONT_5X5[char]
    for r_offset, row_pattern in enumerate(char_pixels):
        for c_offset, pixel_val in enumerate(row_pattern):
            if pixel_val == '1':
                # Add boundary check before drawing
                if 0 <= (start_y + r_offset) < HEIGHT and 0 <= (start_x + c_offset) < WIDTH:
                    # Assuming display.set_xy takes (row, col)
                    display.set_xy((start_y + r_offset, start_x + c_offset), color)

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
                        display.set_xy((y_start + r_offset, current_x + c_offset), color)
            current_x += char_width + char_spacing # Move to the next character position
        else:
            current_x += char_width + char_spacing # Still move even if char not found


def draw_maze():
    """Renders the entire maze, player, start, and destination on the LED-Box."""

    for r in range(HEIGHT):
        for c in range(WIDTH):
            if maze[r][c] == 1: # If it's a wall
                display.set_xy((r, c), COLOR_WALL)
            else: # It's a path
                display.set_xy((r, c), COLOR_PATH)

    # Draw start and destination points
    display.set_xy(tuple(start_pos), COLOR_START)
    display.set_xy(tuple(destination_pos), COLOR_DESTINATION)

    # Draw player
    display.set_xy(tuple(player_pos), COLOR_PLAYER)

    display.show() # Push changes to the physical display

# --- Game Logic ---

def reset_game():
    """Resets the game state, generates a new maze, and places points."""
    global game_active, start_time, game_won_time

    print("[DEBUG] Resetting game...")
    # 1. Generate the maze structure first
    generate_maze_recursive_backtracker()

    # 2. Place start and destination on the generated paths
    place_start_and_destination()

    # 3. Reset game state variables
    game_active = True
    start_time = 0.0 # Reset start time
    game_won_time = 0.0 # Reset won time

    display.fill(COLOR_PATH) # Clear display before drawing new maze
    display.show()
    time.sleep(0.1) # Small delay for clear
    
    # 4. Draw the initial state
    draw_maze()
    print(f"[DEBUG] Game reset. Start: {start_pos}, Destination: {destination_pos}")

def handle_input(key):
    """
    Handles player movement based on remote key presses.
    Checks for walls before moving the player.
    """
    global player_pos, game_active, start_time, game_won_time

    if not game_active and key not in ['ENTER']: # Allow ENTER to reset even if not active
        return # Ignore input if game is over and not a reset command

    new_r, new_c = player_pos[0], player_pos[1] # Using (x,y) or (col, row)
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
    # The player is allowed to move to the exact start_pos or destination_pos, even if they are on the border.
    is_move_to_border_entry = (new_r == start_pos[0] and new_c == start_pos[1])
    is_move_to_border_exit = (new_r == destination_pos[0] and new_c == destination_pos[1])

    if (is_valid_physical_cell(new_r, new_c) and # Check bounds (0 to 15)
        maze[new_r][new_c] == 0): # Check if it's a path

        # Further check: if moving to a border cell (0 or 15), it MUST be the entry/exit point
        if (new_r == 0 or new_r == HEIGHT - 1 or new_c == 0 or new_c == WIDTH - 1) and \
           not (is_move_to_border_entry or is_move_to_border_exit):
            print(f"[DEBUG] Blocked move to perimeter not at entry/exit: ({new_r}, {new_c}).")
            return # Block if it's a border move but not to entry/exit
        
        player_pos[0], player_pos[1] = new_r, new_c
        moved = True
        if start_time == 0.0: # Start timer on first move
            start_time = time.monotonic()
            print("[DEBUG] Game timer started.")
    elif is_valid_physical_cell(new_r, new_c) and maze[new_r][new_c] == 1:
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
    display.fill(COLOR_PATH) # Clear screen
    
    # Display "WIN"
    draw_text(0, 3, "WIN", COLOR_TEXT) # Row 3 is a good vertical center for 5x5 font

    # Display time (e.g., "12.34s")
    time_str = f"{final_time:.1f}s" # Format to 1 decimal place
    
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

    display.show()
    # Game is inactive, will wait for ENTER to reset in game_loop

# --- Remote Input Setup ---

def setup_remote_bindings():
    """Sets up the remote key bindings for player movement."""
    # Clear existing bindings to prevent duplicates
    remote.bindings = {}
    remote.all_binds = []

    # Bind arrow keys to handle_input
    # These key names correspond to what remote_client_maze.py sends
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
    print("Run 'remote_client_maze.py' on your local computer to send inputs (UP, DOWN, LEFT, RIGHT, ENTER).")
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
# Added is_valid_physical_cell as a general utility
def is_valid_physical_cell(r, c):
    """Checks if a given physical coordinate is within the display boundaries."""
    return 0 <= r < HEIGHT and 0 <= c < WIDTH

if __name__ == "__main__":
    # This block is for initial setup specific to the emulator or notebook environment.
    if 'display_emu' in sys.modules and not hasattr(display, 'pixels'):
        print("[DEBUG] Initializing display_emu pixels for notebook environment.")
        try:
            import numpy as np # Ensure numpy is imported if display_emu needs it
            display.pixels = np.zeros((display.height, display.width, 3), dtype=np.uint8)
        except ImportError:
            print("[ERROR] NumPy not found. Emulator display will not work correctly.")
            print("Please ensure your ulib/display.py (emulator) is correctly configured with numpy.")
            display.pixels = [[(0,0,0) for _ in range(display.width)] for _ in range(display.height)]

    game_loop()

