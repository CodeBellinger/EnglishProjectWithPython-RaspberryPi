import socket
import threading

bindings = {}
all_binds = []

def trigger_action(key):
    for action in all_binds:
        action(key)
    if key in bindings:
        for action in bindings[key]:
            action(key)

def listen():
    def handle_packets():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', 5000))
            while True:
                data, addr = s.recvfrom(1024)
                key = data.decode()
                trigger_action(key)

    thread = threading.Thread(target=handle_packets, daemon=True)
    thread.start()

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

listen()
bind_key('A', print)

 # Die Endlosschleife wurde entfernt
 #while True:
 #    # Keep the main thread alive to allow the listener to run
 #    pass