# remote_client.py
import socket
import sys
import msvcrt # Import this at the top of your file
import time
from ulib import display_emu as display  # Replace this with 'from ulib import display' for LEDBox testing

# IP-Adresse deines Raspberry Pis (ersetze DIESE durch die tatsächliche IP!)
# Du findest die IP-Adresse deines Raspberry Pi, indem du `hostname -I`, 'ipconfig', 'nmap 192.168.1.119' im Terminal eingibst.
def map_ip_address():
    """
    Maps IP addresses to ensure consistency between display and display_emu.
    Adjusts the IP address based on the module being used.
    """
    if 'ulib.display_emu' in sys.modules:  # Check if display_emu is imported
        return '127.0.0.1'  # Localhost for testing on the same machine
    else:
        return '192.168.1.119'  # LEDBox for testing on the Raspberry Pi

# Set the IP address for remote communication
RPI_IP = map_ip_address()
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
    print("Use ARROW KEYS (UP, DOWN, LEFT, RIGHT) for movement.")
    print("Use 'ENTER' (or SPACE) to reset the game after winning.")
    print("Press 'Q' to quit (or CTRL+C).")

    while True:
        char = getch() # returns string representations of keys

        if char == 'QUIT_SIGNAL' or char == 'Q':
            print("Quitting client.")
            break

        # Handle arrow keys and Enter
        if char == 'UP_ARROW':
            send_key('UP')
        elif char == 'DOWN_ARROW':
            send_key('DOWN')
        elif char == 'LEFT_ARROW':
            send_key('LEFT')
        elif char == 'RIGHT_ARROW':
            send_key('RIGHT')
        elif char == ' ' or char == '\r': # Space or Enter key
            send_key('ENTER')

        elif not char.startswith("UNKNOWN_BYTE_") and not char.startswith("UNKNOWN_SPECIAL_KEY_SEQUENCE_"):
            print(f"Unknown key: {char}")