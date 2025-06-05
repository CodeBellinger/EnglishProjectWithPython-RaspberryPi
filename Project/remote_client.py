# remote_client.py
import socket
import sys
import msvcrt # Import this at the top of your file

# IP-Adresse deines Raspberry Pis (ersetze DIESE durch die tatsächliche IP!)
# Du findest die IP-Adresse deines Raspberry Pi, indem du `hostname -I` im Terminal eingibst.
RPI_IP = '192.168.1.2'
PORT = 5000

def send_key(key):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(key.encode(), (RPI_IP, PORT))
        print(f"Sent: {key}")

def getch():
    """Reads a single character from stdin without buffering (Windows compatible)."""
    return msvcrt.getch().decode('utf-8') # Decode byte to string

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