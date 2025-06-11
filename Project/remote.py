# remote.py
import socket
import threading
import time

bindings = {}
all_binds = []
listener_thread = None
stop_event = threading.Event() # Event to signal the thread to stop

def trigger_action(key):
    for action in all_binds:
        action(key)
    if key in bindings:
        for action in bindings[key]:
            action(key)

def handle_packets(sock, stop_event):
    """Target function for the listener thread."""
    print("[DEBUG] Remote listener thread started.")
    # Set a timeout for the socket to allow the thread to periodically check the stop_event
    sock.settimeout(0.1) 
    while not stop_event.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            key = data.decode()
            print(f"[DEBUG] Remote received key: {key}") # Debug print for received keys
            trigger_action(key)
        except socket.timeout:
            continue # No data, just check the stop_event again
        except Exception as e:
            # Handle other potential socket errors that should stop the thread
            print(f"[ERROR] Remote listener error: {e}")
            break # Exit on error
    sock.close() # Close the socket when the thread stops
    print("[DEBUG] Remote listener thread stopped and socket closed.")


def start_listening():
    global listener_thread, stop_event
    if listener_thread is not None and listener_thread.is_alive():
        print("[DEBUG] Remote listener already running.")
        return # Already listening, do nothing

    stop_event.clear() # Clear any previous stop signal
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(('', 5000))
        print("[DEBUG] Remote socket bound to port 5000.")
    except OSError as e:
        print(f"[ERROR] Failed to bind socket: {e}. Port 5000 might be in use. Please ensure no other process is using it or restart your kernel.")
        s.close()
        return # Cannot start listener
    
    listener_thread = threading.Thread(target=handle_packets, args=(s, stop_event), daemon=True)
    listener_thread.start()
    print("[DEBUG] Remote listener thread launched.")


def stop_listening():
    global listener_thread, stop_event
    if listener_thread and listener_thread.is_alive():
        print("[DEBUG] Signalling remote listener to stop...")
        stop_event.set() # Signal the thread to stop
        # Give a small moment for the thread to exit cleanly
        listener_thread.join(timeout=1.0) # Wait up to 1 second for thread to finish
        if listener_thread.is_alive():
            print("[WARNING] Remote listener thread did not stop gracefully. You may need to restart your kernel.")
        else:
            print("[DEBUG] Remote listener thread joined successfully.")
    
    # Reset for next time `start_listening` is called
    listener_thread = None
    stop_event.clear()


def bind_key(key, action):
    if key not in bindings:
        bindings[key] = []
    bindings[key].append(action)

def unbind_key(key, action):
    if key in bindings and action in bindings[key]:
        bindings[key].remove(action)
        if not bindings[key]:
            del bindings[key]

def bind_all(action):
    all_binds.append(action)

def unbind_all(action):
    if action in all_binds:
        all_binds.remove(action)

# IMPORTANT: No direct call to listen() or bind_key() here anymore.
# They will be called from connect4.py