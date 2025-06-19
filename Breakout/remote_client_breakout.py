# remote_client_breakout.py
# Sendet Tastatureingaben an den Raspberry Pi oder den lokalen Game-Loop-Server
# für das Breakout-Spiel.

import socket
import sys
import msvcrt # Nur für Windows, für Unix/Linux 'import termios, tty' verwenden

# IP-Adresse deines Raspberry Pis (ersetze DIESE durch die tatsächliche IP!)
# Du findest die IP-Adresse deines Raspberry Pi, indem du `hostname -I` im Terminal eingibst.
# Oder für lokalen Test auf demselben PC: '127.0.0.1'
RPI_IP = '127.0.0.1' # Ändere dies zu deiner Pi-IP, wenn du auf dem Pi spielst
PORT = 5000

def send_key(key):
    """Sendet einen Schlüsselbefehl über UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(key.encode(), (RPI_IP, PORT))
        print(f"Sent: {key}")

def getch():
    """
    Liest ein einzelnes Zeichen oder eine Sondertaste von stdin ohne Pufferung.
    (Windows-kompatibel).
    Für Linux/macOS müsste hier `termios` und `tty` verwendet werden.
    """
    if sys.platform == "win32":
        char = msvcrt.getch() # Liest Byte(s)

        if char == b'\x03': # Ctrl+C (ETX) wird zum Signal für ein sauberes Beenden verwendet
            return 'QUIT_SIGNAL'

        # Prüfe auf spezielle Tastenfolgen (erstes Byte ist 0x00 oder 0xE0)
        if char == b'\x00' or char == b'\xe0':
            second_char = msvcrt.getch() # Liest das zweite Byte der Sequenz
            if second_char == b'K': # Linker Pfeil
                return 'LEFT_ARROW'
            elif second_char == b'M': # Rechter Pfeil
                return 'RIGHT_ARROW'
            # Weitere Pfeiltasten oder Sondertasten können hier hinzugefügt werden
            elif second_char == b'H': # Up Arrow (optional, falls benötigt)
                return 'UP_ARROW'
            elif second_char == b'P': # Down Arrow (optional, falls benötigt)
                return 'DOWN_ARROW'
            # Füge hier bei Bedarf weitere spezielle Tastenbehandlungen hinzu (z.B. F-Tasten)
            return f"UNKNOWN_SPECIAL_KEY_SEQUENCE_{second_char.hex()}" # Für unbehandelte Sondertasten

        # Für Standardtasten, versuche, zu UTF-8 zu dekodieren und in Großbuchstaben umzuwandeln
        try:
            return char.decode('utf-8').upper()
        except UnicodeDecodeError:
            # Falls es ein einzelnes Byte ist, das kein gültiges UTF-8 ist, oder unerwartet ist.
            return f"UNKNOWN_BYTE_{char.hex()}" # Gibt einen eindeutigen String für unbekannte Bytes zurück
    else: # Für Linux/macOS
        # Dies ist eine vereinfachte Version für Nicht-Windows-Systeme.
        # Eine robustere Lösung würde termios und tty für non-blocking input verwenden.
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == '\x03': # Ctrl+C
            return 'QUIT_SIGNAL'
        if ch == '\x1b': # Escape sequence for arrow keys
            ch += sys.stdin.read(2)
            if ch == '\x1b[A': return 'UP_ARROW'
            if ch == '\x1b[B': return 'DOWN_ARROW'
            if ch == '\x1b[C': return 'RIGHT_ARROW'
            if ch == '\x1b[D': return 'LEFT_ARROW'
        return ch.upper()


if __name__ == "__main__":
    print(f"Sending commands to {RPI_IP}:{PORT}")
    print("Use 'A' (Left), 'D' (Right), 'SPACE' (Enter) for Paddle movement and ball launch.")
    print("Press 'Q' to quit (or CTRL+C).")

    while True:
        char = getch() # returns string representations of keys

        if char == 'QUIT_SIGNAL' or char == 'Q':
            print("Quitting client.")
            break

        if char == 'A':
            send_key('LEFT')
        elif char == 'D':
            send_key('RIGHT')
        elif char == ' ': # Leertaste für ENTER
            send_key('ENTER')
        # Für Debugging oder alternative Steuerung:
        elif char == 'LEFT_ARROW':
            send_key('LEFT')
        elif char == 'RIGHT_ARROW':
            send_key('RIGHT')
        elif char == '\r': # Standard Enter-Taste
            send_key('ENTER')