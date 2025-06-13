# main_connect4.py
# If viergewinnt.py is executed directly from within the 'Project' folder,
# or if 'Project' is added to sys.path, then direct imports are fine.
from . import display_emu # Oder display für Raspberry Pi
import time
from . import remote
import random
import math

# Konstanten
WIDTH = 16
HEIGHT = 16 # Display-Höhe
BOARD_COLS = 16 # Spielfeld Spalten
BOARD_ROWS = 15 # Spielfeld Reihen (1 Reihe für fallenden Chip, 7 für Spiel)

PLAYER1_COLOR = (255, 0, 0) # Rot
PLAYER2_COLOR = (0, 0, 255) # Blau
EMPTY_COLOR = (0, 0, 0)   # Schwarz
GRID_COLOR = (50, 50, 50) # Optional: für leere Felder

# Function to get a lighter version of a player's color for the ghost chip
def get_ghost_color(player_color, transparency_factor=0.4):
    """Returns a lighter/more transparent version of a given color."""
    r, g, b = player_color
    return (
        int(r + (255 - r) * transparency_factor),
        int(g + (255 - g) * transparency_factor),
        int(b + (255 - b) * transparency_factor)
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
game_board = [[EMPTY_COLOR for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
current_col = 0 # Current column selected by player
current_player = 1 # 1 or 2
game_over = False
winner = None

# Helper function to find the next empty row in a column
def get_landing_row(col):
    for r in range(BOARD_ROWS -1, -1, -1): # Iterate from bottom up
        if game_board[r][col] == EMPTY_COLOR:
            return r
    return -1 # Column is full

def draw_board():
    global game_board, current_col, current_player

    # 1. Clear the entire display or fill with background (optional, but good for clean redraws)
    display_emu.fill(EMPTY_COLOR)  # Clear the entire display

    # 2. Draw the chip in the first rank
    chip_color = PLAYER1_COLOR if current_player == 1 else PLAYER2_COLOR
    display_emu.set_xy(current_col, 0, chip_color)  # Display chip in the first rank

    # 3. Draw Ghost Chip
    if not game_over:  # Only show ghost chip if the game is active
        landing_row = get_landing_row(current_col)
        if landing_row != -1:  # If the column is not full
            ghost_color = PLAYER1_GHOST_COLOR if current_player == 1 else PLAYER2_GHOST_COLOR
            display_emu.set_xy(current_col, landing_row, ghost_color)

    # 4. Draw Actual Game Chips (these will overwrite the ghost chip where chips exist)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            color = game_board[r][c]
            if color != EMPTY_COLOR:
                display_emu.set_xy(c, r, color)

    # 4. Update the physical display
    display_emu.show()

def drop_chip(col, player):
    global game_over, winner

    for r in range(BOARD_ROWS - 1, -1, -1):
        if board[r][col] == 0:
            chip_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
            for current_display_y in range(0, (HEIGHT - BOARD_ROWS) + r + 1):
                display_emu.fill(EMPTY_COLOR)
                draw_board_without_preview() # This also needs to use (x,y) now
                
                # OLD: display_emu.set_xy((current_display_y, col), chip_color) # This was the (y,x) swap
                # NEW: Back to (x, y) after display_emu refactor
                display_emu.set_xy(col, current_display_y, chip_color) 
                
                display_emu.show()
                time.sleep(0.05)
            
            board[r][col] = player
            return True
    return False

def draw_board_without_preview():
    display_emu.fill(EMPTY_COLOR)

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            pixel_color = EMPTY_COLOR
            if board[r][c] == 1:
                pixel_color = PLAYER1_COLOR
            elif board[r][c] == 2:
                pixel_color = PLAYER2_COLOR
            
            display_y = (HEIGHT - BOARD_ROWS) + r
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

def check_win(board, player):
    # Horizontale Überprüfung
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Vertikale Überprüfung
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Diagonale (von unten links nach oben rechts)
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Diagonale (von oben links nach unten rechts)
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
    return False

def is_board_full():
    for c in range(BOARD_COLS):
        if board[0][c] == 0: # Check the top row for any empty spot
            return False
    return True

def handle_input(key):
    global selected_column, current_player, game_over, winner

    if game_over:
        if key == 'ENTER': # Reset game
            reset_game()
        return

    if key == 'LEFT':
        selected_column = max(0, selected_column - 1)
    elif key == 'RIGHT':
        selected_column = min(BOARD_COLS - 1, selected_column + 1)
    elif key == 'ENTER':
        if drop_chip(selected_column, current_player):
            if check_win(board, current_player):
                winner = current_player
                game_over = True
            elif is_board_full():
                winner = 0 # Draw
                game_over = True
            else:
                current_player = 3 - current_player # Wechselt zwischen 1 und 2
        else:
            print("Spalte ist voll!") # Kannst du auch auf dem Display anzeigen lassen

def reset_game():
    global board, current_player, selected_column, game_over, winner
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_player = 1
    selected_column = 0
    game_over = False
    winner = None
    display_emu.fill(EMPTY_COLOR) # Lösche das Display

def game_loop():
    global current_player, selected_column, game_over, winner

    # Initialisierung des Spiels
    remote.bind_all(handle_input) # Registriert handle_input für alle Tasten
    draw_board()

    # Hauptspielschleife
    while True:
        draw_board()
        if game_over:
            if winner == 1:
                print("Spieler 1 gewinnt!")
                # Run fireworks and winner text for Player 1
                animate_fireworks(PLAYER1_COLOR)
                animate_winner_text(PLAYER1_COLOR, 1)
            elif winner == 2:
                print("Spieler 2 gewinnt!")
                # Run fireworks and winner text for Player 2
                animate_fireworks(PLAYER2_COLOR)
                animate_winner_text(PLAYER2_COLOR, 2)
            else: # Unentschieden
                print("Unentschieden!")
                # For a draw, perhaps a simple white fade or specific draw animation
                for _ in range(3): # Simple white blink for draw
                    display_emu.fill((255,255,255))
                    display_emu.show()
                    time.sleep(0.8)
                    display_emu.fill(EMPTY_COLOR)
                    display_emu.show()
                    time.sleep(0.3)
                # Or you could add a "DRAW!" text animation here if you define more characters in FONT_5X5
                # animate_winner_text((255,255,255), "DRAW") # If you make a "DRAW" case
            
            print("Drücke ENTER zum Neustart.")
            # ... (rest of game_over loop - keep the while game_over: time.sleep(0.1) part) ...

# Im viergewinnt.py (oder in einem separaten Setup-Block, der nach dem Import läuft)

# Bindungen für Spieler 1 (z.B. A, D, W)
remote.bind_key('A', lambda key: handle_input('LEFT'))    # Spieler 1: 'A' bewegt nach links
remote.bind_key('D', lambda key: handle_input('RIGHT'))   # Spieler 1: 'D' bewegt nach rechts
remote.bind_key('SPACE', lambda key: handle_input('ENTER'))   # Spieler 1: 'W' (oder eine andere Taste) lässt Chip fallen

# Bindungen für Spieler 2 (z.B. J, L, I)
# Beachte: Dies erfordert, dass handle_input die Unterscheidung zwischen Spielern vornimmt
# Aktuell nimmt handle_input den ausgewählten Chip und droppt ihn.
# Für 2 Spieler müsstest du handle_input so anpassen, dass es den aktuellen Spieler berücksichtigt,
# oder separate Funktionen für jeden Spieler haben, die dann gebunden werden.
# Fürs Erste nehmen wir an, dass handle_input immer den aktuellen Spieler steuert.
# Wenn beide Spieler gleichzeitig eingeben, könnte es zu Konflikten kommen,
# da die Logik für "current_player" global ist.
# Für eine vollständige 2-Spieler-Steuerung über Remote, die Spieler unterscheidet,
# müsste die Logik in viergewinnt.py erweitert werden.

# Beispiel für 2-Spieler-Steuerung (wenn handle_input den aktuellen Spieler steuert):
# Die game_loop in viergewinnt.py wechselt den Spieler automatisch.
# Die Remote-Eingaben steuern dann den jeweils aktiven Spieler.

# Bindungen für Spieler 2 (standardisierte Tasten LEFT, RIGHT, ENTER -
# diese müssten dann vom Client gesendet werden, z.B. als 'LEFT2', 'RIGHT2', 'ENTER2'
# und handle_input müsste angepasst werden, um 'LEFT', 'LEFT2' etc. zu verarbeiten)

# ODER: Wenn du nur EINE Tastatur hast, die abwechselnd steuert, bleiben die obigen 'A','D','W' Bindungen
# und die Spieler wechseln sich mit dieser Tastatur ab.
# Wenn ZWEI separate Quellen steuern sollen, brauchst du eine erweiterte handle_input Logik.

# Für das aktuelle Spiel, das den current_player global verwaltet:
# Es ist am einfachsten, wenn die Remote-Befehle die gleichen sind wie die internen ('LEFT', 'RIGHT', 'ENTER').
# Das remote.py empfängt dann diese Strings.

# Stelle sicher, dass diese Bindungen NUR einmal ausgeführt werden,
# z.B. wenn das Spiel startet.
remote.bind_key('LEFT', lambda key: handle_input('LEFT'))
remote.bind_key('RIGHT', lambda key: handle_input('RIGHT'))
remote.bind_key('ENTER', lambda key: handle_input('ENTER'))

# Wenn du einen Reset per Remote ermöglichen willst (was bereits in viergewinnt.py angedeutet ist):
# remote.bind_key('RESET', lambda key: viergewinnt.reset_game())
# Und die handle_input Funktion in viergewinnt.py müsste entsprechend angepasst werden,
# um 'ENTER' auch für den Neustart zu nutzen, wenn game_over ist.
# Dies ist bereits in viergewinnt.py im game_over Block angedeutet:
# print("Drücke ENTER zum Neustart.")
# Du müsstest sicherstellen, dass dein handle_input() diese Logik auch für remote-ENTER-Inputs ausführt.
# Die aktuelle Struktur in viergewinnt.py scheint bereits darauf ausgelegt zu sein,
# dass `handle_input` (egal ob lokal oder remote aufgerufen) den Game-State korrekt aktualisiert,
# inklusive Reset bei Game Over.

if __name__ == '__main__':
    game_loop() # Oder rufe deine Hauptfunktion auf, die das Spiel startet