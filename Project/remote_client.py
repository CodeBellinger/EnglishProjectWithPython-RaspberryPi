# remote_client.py
import socket
import sys
import termios # Only for Linux/macOS
import tty    # Only for Linux/macOS

# IP-Adresse deines Raspberry Pis (ersetze DIESE durch die tatsächliche IP!)
# Du findest die IP-Adresse deines Raspberry Pi, indem du `hostname -I` im Terminal eingibst.
RPI_IP = 'DEINE_RASPBERRY_PI_IP'
PORT = 5000

def send_key(key):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(key.encode(), (RPI_IP, PORT))
        print(f"Sent: {key}")

def getch():
    """Reads a single character from stdin without buffering."""
    # This function is platform-dependent.
    # On Windows, you might use `msvcrt.getch()`.
    # This example is for Linux/macOS.
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    print(f"Sending commands to {RPI_IP}:{PORT}")
    print("Use 'A' (Left), 'D' (Right), 'SPACE' (Enter) for Player 1.")
    print("Use 'J' (Left), 'L' (Right), 'I' (Enter) for Player 2 (if game supports distinct inputs).")
    print("Press 'Q' to quit.")

    while True:
        char = getch().upper() # Read character and convert to uppercase

        if char == 'A':
            send_key('LEFT')
        elif char == 'D':
            send_key('RIGHT')
        elif char == 'SPACE':
            send_key('ENTER')
        elif char == 'J': # Beispiel für Spieler 2-Steuerung
            send_key('LEFT') # Oder 'LEFT2' wenn handle_input das unterscheiden soll
        elif char == 'L': # Beispiel für Spieler 2-Steuerung
            send_key('RIGHT') # Oder 'RIGHT2'
        elif char == 'I': # Beispiel für Spieler 2-Steuerung
            send_key('ENTER') # Oder 'ENTER2'
        elif char == 'Q':
            print("Quitting client.")
            break
        else:
            print(f"Unknown key: {char}")