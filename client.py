import socket

host = '127.0.0.1'  
port = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def get_data():
    raw = s.recv(4096)
    data = int(raw.decode('utf-8'))
    return data
    

while True: #this will likely be an update function in the backend
    data = get_data()
    print(f'from socket: {data}')
