# breakout.py
# Ein Breakout-Spiel für die 16x16 LED-Box mit ulib-Bibliotheken

# --- Import-Anpassung für Emulator vs. Hardware ---
# Wähle EINEN der folgenden Imports:
# Für die lokale Emulation (auf deinem PC):
from ulib import display_emu as display
import numpy as np # Importiere numpy explizit für den Emulator

# Für die Ausführung auf dem Raspberry Pi (Hardware):
# from ulib import display
# (Hier KEIN numpy importieren, da es auf dem Pi in display.py nicht benötigt wird)
# ----------------------------------------------------

from ulib import remote
import time
import random
import math # Für komplexere Ballphysik, falls benötigt

# --- Konstanten ---
WIDTH = 16
HEIGHT = 16

# Farben (RGB-Tupel)
COLOR_BACKGROUND = (0, 0, 0)      # Schwarz
COLOR_PADDLE = (0, 255, 0)        # Grün
COLOR_BALL = (255, 255, 0)        # Gelb
COLOR_BRICK_1 = (255, 0, 0)       # Rot
COLOR_BRICK_2 = (0, 0, 255)       # Blau
COLOR_BRICK_3 = (255, 128, 0)     # Orange
COLOR_GAME_OVER = (255, 0, 0)     # Rot für Game Over
COLOR_WIN = (0, 255, 0)           # Grün für Win

# Spielparameter
PADDLE_WIDTH = 4
PADDLE_HEIGHT = 1
PADDLE_Y = HEIGHT - 2 # Zweite Reihe von unten

BALL_START_X = WIDTH // 2
BALL_START_Y = HEIGHT - 3 # Über dem Paddel

INITIAL_LIVES = 3
BRICK_ROWS = 4
BRICK_COLS = 8 # Halbe Breite des Displays, damit die Blöcke einzeln sind

# --- Spielzustand-Variablen ---
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
ball_x, ball_y = BALL_START_X, BALL_START_Y
ball_dx, ball_dy = random.choice([-1, 1]), -1 # Initial: nach oben links/rechts
lives = INITIAL_LIVES
bricks = [] # Liste von (x, y, color) für jeden Ziegel
game_over = False
game_won = False
score = 0
last_update_time = 0
game_active = False # Flag um Spielpause nach Start/Win/Lose zu steuern

# --- Font (Optional, für WIN/LOSE Text) ---
FONT_5X5 = {
    'W': ["10101", "10101", "10101", "10101", "01010"],
    'I': ["11111", "01000", "01000", "01000", "11111"],
    'N': ["11000", "10100", "10010", "10001", "10001"],
    'L': ["10000", "10000", "10000", "10000", "11111"],
    'O': ["01110", "10001", "10001", "10001", "01110"],
    'S': ["01111", "10000", "01110", "00001", "11110"],
    'E': ["11111", "10000", "11110", "10000", "11111"],
    'G': ["01110", "10000", "10110", "10001", "01110"],
    'M': ["11111", "01010", "00100", "01010", "11111"], # A bit crude for 5x5
    'V': ["10001", "10001", "01010", "01010", "00100"],
    'R': ["11110", "10001", "11110", "10010", "10001"]
}

def draw_char(char, start_x, start_y, color):
    """Zeichnet ein 5x5 Zeichen auf dem Display."""
    if char not in FONT_5X5:
        return
    for r_idx, row_str in enumerate(FONT_5X5[char]):
        for c_idx, pixel_char in enumerate(row_str):
            if pixel_char == '1':
                display.set_xy((start_x + c_idx, start_y + r_idx), color)

def draw_text(text, start_x, start_y, color, char_spacing=1):
    """Zeichnet eine Zeichenkette auf dem Display."""
    current_x = start_x
    for char in text.upper():
        if char == ' ': # Handle space
            current_x += 5 + char_spacing
            continue
        draw_char(char, current_x, start_y, color)
        current_x += 5 + char_spacing # 5 is character width

# --- Hilfsfunktionen ---
def reset_game():
    """Setzt das Spiel in den Ausgangszustand zurück."""
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, lives, bricks, game_over, game_won, score, game_active

    display.fill(COLOR_BACKGROUND)
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    ball_x, ball_y = BALL_START_X, BALL_START_Y
    ball_dx = random.choice([-1, 1])
    ball_dy = -1 # Immer zuerst nach oben
    lives = INITIAL_LIVES
    score = 0
    game_over = False
    game_won = False
    game_active = False # Spiel beginnt in "Pause"-Zustand

    # Blöcke generieren
    bricks.clear()
    brick_colors = [COLOR_BRICK_1, COLOR_BRICK_2, COLOR_BRICK_3]
    for r in range(BRICK_ROWS):
        for c in range(BRICK_COLS):
            # Berechne x- und y-Koordinate für den Block
            # Kleine Lücke zwischen den Blöcken und Rand
            brick_x = 1 + c * (WIDTH // BRICK_COLS)
            brick_y = 1 + r
            bricks.append((brick_x, brick_y, random.choice(brick_colors)))
    display.show()
    print("[DEBUG] Game reset. Press ENTER to start.")

def draw_game_elements():
    """Zeichnet alle Spielelemente auf das Display."""
    display.fill(COLOR_BACKGROUND) # Alles löschen

    # Paddel zeichnen
    for i in range(PADDLE_WIDTH):
        display.set_xy((paddle_x + i, PADDLE_Y), COLOR_PADDLE)

    # Ball zeichnen
    display.set_xy((ball_x, ball_y), COLOR_BALL)

    # Blöcke zeichnen
    for brick_x, brick_y, color in bricks:
        display.set_xy((brick_x, brick_y), color)

    display.show()

def update_game_state():
    """Aktualisiert den Spielzustand (Ballbewegung, Kollisionen)."""
    global ball_x, ball_y, ball_dx, ball_dy, lives, game_over, game_won, score

    if not game_active:
        return

    # Ballbewegung
    new_ball_x = ball_x + ball_dx
    new_ball_y = ball_y + ball_dy

    # Kollision mit Wänden
    if new_ball_x <= 0 or new_ball_x >= WIDTH - 1:
        ball_dx *= -1
        new_ball_x = ball_x + ball_dx # Korrigiere Position, um im Bereich zu bleiben
    if new_ball_y <= 0: # Oberer Rand
        ball_dy *= -1
        new_ball_y = ball_y + ball_dy

    # Kollision mit Paddel
    if new_ball_y == PADDLE_Y - 1 and paddle_x <= new_ball_x < paddle_x + PADDLE_WIDTH:
        ball_dy *= -1
        # Optional: Ballrichtung basierend auf Auftreffpunkt ändern
        hit_pos = new_ball_x - paddle_x
        if hit_pos == 0: # Ganz links
            ball_dx = -1
        elif hit_pos == PADDLE_WIDTH - 1: # Ganz rechts
            ball_dx = 1
        # In der Mitte bleibt dx gleich
        new_ball_y = ball_y + ball_dy # Korrigiere Position

    # Kollision mit Blöcken
    brick_hit_index = -1
    for i, (brick_x, brick_y, _) in enumerate(bricks):
        # Einfache Kollision: Ball ist im gleichen Pixel wie der Block
        if new_ball_x == brick_x and new_ball_y == brick_y:
            brick_hit_index = i
            break

    if brick_hit_index != -1:
        bricks.pop(brick_hit_index) # Block entfernen
        score += 10
        ball_dy *= -1 # Ball prallt ab
        new_ball_y = ball_y + ball_dy # Korrigiere Position
        print(f"[DEBUG] Brick hit! Score: {score}")

    # Unterer Rand (Verlust eines Lebens)
    if new_ball_y >= HEIGHT - 1:
        lives -= 1
        print(f"[DEBUG] Ball out! Lives left: {lives}")
        if lives <= 0:
            game_over = True
            print("[DEBUG] Game Over!")
        else:
            # Ball und Paddel zurücksetzen für das nächste Leben
            ball_x, ball_y = BALL_START_X, BALL_START_Y
            ball_dx = random.choice([-1, 1])
            ball_dy = -1
            paddle_x = (WIDTH - PADDLE_WIDTH) // 2
            game_active = False # Spiel pausieren bis ENTER gedrückt wird

    ball_x = new_ball_x
    ball_y = new_ball_y

    # Prüfen, ob alle Blöcke zerstört sind
    if not bricks and not game_over:
        game_won = True
        print("[DEBUG] You Win!")

def handle_input(key):
    """Verarbeitet Eingaben vom Remote-Client."""
    global paddle_x, game_active, game_over, game_won

    if game_over or game_won:
        if key == 'ENTER':
            reset_game()
            game_active = True # Spiel direkt starten nach Reset bei Win/Lose
            print("[DEBUG] Game restarted.")
        return

    if key == 'LEFT':
        paddle_x = max(0, paddle_x - 1)
        # print(f"[DEBUG] Paddle left to {paddle_x}")
    elif key == 'RIGHT':
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + 1)
        # print(f"[DEBUG] Paddle right to {paddle_x}")
    elif key == 'ENTER':
        if not game_active:
            game_active = True
            print("[DEBUG] Game started!")

# --- Hauptspiel-Loop ---
def game_loop():
    """Die Hauptspielschleife."""
    global last_update_time

    remote.start_listening() # Starte den Remote-Listener
    setup_remote_bindings() # Binde Tasten an Aktionen

    print("--- Starting Breakout Game ---")
    print("Use a separate terminal to run remote_client_breakout.py.")
    print("Controls: 'A' (Left), 'D' (Right), 'SPACE' (Enter).")
    print("Press 'ENTER' to start the ball or reset the game after game over/win.")
    print("To stop this game loop, interrupt the kernel (Square Stop button above or Kernel -> Interrupt).")

    reset_game() # Initiales Setup

    try:
        while True:
            current_time = time.time()
            if game_active and current_time - last_update_time > 0.15: # Ballgeschwindigkeit
                update_game_state()
                last_update_time = current_time

            draw_game_elements()

            if game_over:
                draw_text("GAME", 2, 5, COLOR_GAME_OVER)
                draw_text("OVER", 2, 10, COLOR_GAME_OVER)
                display.show()
                time.sleep(0.5) # Warte, bis Enter zum Neustart gedrückt wird
            elif game_won:
                draw_text("YOU", 2, 5, COLOR_WIN)
                draw_text("WIN", 2, 10, COLOR_WIN)
                display.show()
                time.sleep(0.5) # Warte, bis Enter zum Neustart gedrückt wird

            time.sleep(0.01) # Kleine Pause, um CPU zu entlasten und Display-Updates zu ermöglichen

    except KeyboardInterrupt:
        print("\n--- Game loop interrupted by user. ---")
    finally:
        print("[DEBUG] Game loop ending. Stopping remote listener.")
        remote.stop_listening() # Stelle sicher, dass der Listener beendet wird

# --- Remote-Binding Setup ---
def setup_remote_bindings():
    """Setzt die Remote-Tastenbindungen für das Spiel."""
    # Bestehende Bindungen löschen, um Duplikate zu vermeiden, falls dies mehrmals aufgerufen wird
    remote.bindings = {}
    remote.all_binds = []

    # Tasten für Spieler 1
    remote.bind_key('LEFT', lambda key: handle_input('LEFT'))
    remote.bind_key('RIGHT', lambda key: handle_input('RIGHT'))
    remote.bind_key('ENTER', lambda key: handle_input('ENTER'))
    print("[DEBUG] Remote bindings set up for Breakout.")

# --- Spiel starten, wenn das Skript direkt ausgeführt wird ---
if __name__ == "__main__":
    # Wenn du den Emulator verwendest und numpy im display_emu nicht direkt importiert ist,
    # musst du es hier initialisieren (nur für den Emulator relevant).
    # Das connect4.ipynb Notebook macht das in einer separaten Zelle,
    # hier machen wir es direkt, wenn display_emu verwendet wird.
    if 'display_emu' in sys.modules and hasattr(display, 'pixels') and display.pixels.shape != (display.height, display.width, 3):
        print("[DEBUG] Initializing display_emu pixels for notebook environment.")
        display.pixels = np.zeros((display.height, display.width, 3), dtype=np.uint8)

    game_loop()