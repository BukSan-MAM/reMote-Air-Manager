import socketio
import subprocess
import psutil
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SERVER_URL = os.getenv('FLASK_SERVER_URL')

def killProcess(pid):
    subprocess.Popen('taskkill /F /PID {0}'.format(pid), shell=True)

# 서버 URL
server_url = FLASK_SERVER_URL
main_pid = None

# SocketIO 클라이언트 생성
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('execute_command')
def on_execute_command(command):
    print(f"Executing command: {command}")
    try:
        cmd_array = command.split(' ')
        print(f'cmd_array: {cmd_array}')
        extProc = subprocess.Popen(cmd_array) # runs main.py
        print(f'extProc: {extProc}')
        status = subprocess.Popen.poll(extProc) # status should be 'None'
        print(f'status: {status}')

        global main_pid
        main_pid = extProc.pid
        print(f'main_pid: {main_pid}')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        print(f'error: {output}')
    # print(f"Command result:\n{output}")

@sio.on('terminate_command')
def on_terminate_command():
    try:
        global main_pid
        if main_pid == None:
            print('error: main_pid should not be None')
        killProcess(main_pid)
        print(f'terminate extProc: {main_pid}')
        status = subprocess.Popen.poll(main_pid) # status should now be something other than 'None' ('1' in my testing)
        print(f'terminate status: {status}')
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    print("main.py process not found.")

@sio.on('listener_on_command')
def on_listener_on_command(command):
    print(f"Listner on command: {command}")
    try:
        cmd_array = command.split(' ')
        print(f'cmd_array: {cmd_array}')
        extProc = subprocess.Popen(cmd_array) # runs main.py
        print(f'extProc: {extProc}')
        status = subprocess.Popen.poll(extProc) # status should be 'None'
        print(f'status: {status}')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        print(f'error: {output}')

if __name__ == '__main__':
    # 서버에 연결
    sio.connect(server_url)
    sio.wait()
