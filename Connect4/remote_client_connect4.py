# remote_client_connect4.py
import socket
import sys
import msvcrt # Import this at the top of your file

# IP-Adresse deines Raspberry Pis (ersetze DIESE durch die tatsächliche IP!)
# Du findest die IP-Adresse deines Raspberry Pi, indem du `hostname -I`, 'ipconfig', 'nmap 192.168.1.119' im Terminal eingibst.
RPI_IP = '127.0.0.1' # Localhost for testing on the same machine
#RPI_IP = '192.168.1.119'
PORT = 5000

def send_key(key):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(key.encode(), (RPI_IP, PORT))
        print(f"Sent: {key}")

def getch():
    """Reads a single character or special key from stdin without buffering (Windows compatible)."""
    char = msvcrt.getch() # Read byte(s)

    if char == b'\x03': # Ctrl+C (ETX) is used to signal a graceful exit
        return 'QUIT_SIGNAL'

    # Check for special key sequences (first byte is 0x00 or 0xE0)
    if char == b'\x00' or char == b'\xe0':
        second_char = msvcrt.getch() # Read the second byte of the sequence
        if second_char == b'K': # Left Arrow
            return 'LEFT_ARROW'
        elif second_char == b'M': # Right Arrow
            return 'RIGHT_ARROW'
        elif second_char == b'H': # Up Arrow (if you need it)
            return 'UP_ARROW'
        elif second_char == b'P': # Down Arrow (often used as 'Enter' or action in games)
            return 'DOWN_ARROW'
        # Add more special key handling here if needed (e.g., F-keys)
        return f"UNKNOWN_SPECIAL_KEY_SEQUENCE_{second_char.hex()}" # For unhandled special keys
    
    # For standard keys, try to decode to UTF-8 and convert to uppercase
    try:
        return char.decode('utf-8').upper()
    except UnicodeDecodeError:
        # If it's a single byte that's not valid UTF-8, or unexpected.
        return f"UNKNOWN_BYTE_{char.hex()}" # Return a unique string for unknown bytes

if __name__ == "__main__":
    print(f"Sending commands to {RPI_IP}:{PORT}")
    print("Use 'A' (Left), 'D' (Right), 'SPACE' (Enter) for Player 1.")
    print(" Use 'LEFT ARROW' (Left), 'RIGHT ARROW' (Right), 'DOWN ARROW' (Enter) for Player 2.")
    print("Press 'Q' to quit (or CTRL+C).")

    while True:
        char = getch() # returns string representations of keys

        if char == 'QUIT_SIGNAL' or char == 'Q':
            print("Quitting client.")
            break
        # Player 1 controls (using arrow keys for distinct actions)
        if char == 'A':
            send_key('LEFT')
        elif char == 'D':
            send_key('RIGHT')
        elif char == ' ':
            send_key('ENTER')

        # Player 2 controls (using arrow keys for distinct actions)
        elif char == 'LEFT_ARROW':
            send_key('P2_LEFT') # Sends a distinct command for Player 2 left
        elif char == 'RIGHT_ARROW':
            send_key('P2_RIGHT') # Sends a distinct command for Player 2 right
        elif char == 'DOWN_ARROW': # Map Down Arrow to Player 2's "ENTER" action
            send_key('P2_ENTER') # Sends a distinct command for Player 2 enter
        elif char == '\r': # Standard Enter key (carriage return) for Player 2
            send_key('P2_ENTER') # Also map standard Enter key to P2_ENTER

        elif char == 'Q':
            print("Quitting client.")
            break
        
        elif not char.startswith("UNKNOWN_BYTE_") and not char.startswith("UNKNOWN_SPECIAL_KEY_SEQUENCE_"):
            print(f"Unknown key: {char}")