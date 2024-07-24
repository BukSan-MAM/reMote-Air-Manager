import sys
import socketio
import time
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SERVER_URL = os.getenv('FLASK_SERVER_URL')
# URL
server_url = FLASK_SERVER_URL

# SocketIO
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

def send_execute_command():
    sio.emit('send_execute_command')
    
def send_terminate_command():
    sio.emit('send_terminate_command')

def send_listener_on_command():
    sio.emit('send_listener_on_command')

if __name__ == '__main__':
    # connect to flask server
    sio.connect(server_url)

    if len(sys.argv) != 2:
        print("Usage: python3 command_manager.py <keyboard-listener-?on|off>")
        sys.exit(1)
    
    command = sys.argv[1].lower()

    # emit command to server
    if command == 'on':
        send_execute_command()
    elif command == 'off':
        send_terminate_command()
    elif command == 'keyboard-listener-on':
        send_listener_on_command()
    else: 
        print("Invalid command. Use 'mouse|keyboard-on|off'.")
        sys.exit(1)
    
    # Wait for a short time to ensure the command is sent
    time.sleep(2)  # Adjust the sleep time as necessary

    # Disconnect from the server
    sio.disconnect()