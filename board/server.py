from flask import Flask
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Flask SocketIO Server is running."

@socketio.on('send_execute_command')
def handle_send_command():
    command = 'python control_mouse.py'
    print(f"Received execute command")
    emit('execute_command', command, broadcast=True, include_self=False)
    print(f'emitted command')

@socketio.on('send_terminate_command')
def handle_send_command():
    print(f"Received terminate command")
    emit('terminate_command', broadcast=True, include_self=False)
    print(f'emitted command')

@socketio.on('send_listener_on_command')
def handle_send_command():
    command = 'python control_keyboard.py'
    print(f"Received listener on command")
    emit('listener_on_command', command, broadcast=True, include_self=False)
    print(f'emitted command')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
