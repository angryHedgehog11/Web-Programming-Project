from http import server
from pydoc import cli
import socket 
import pickle 

HEADERSIZE = 10
PORT = 1000 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

msg_n = int(input())
msg_n = str(msg_n)
client.send(msg_n.encode())

while True: 
    full_msg = b''
    new_msg = True 
    while True: 
        msg = client.recv(2048)
        if new_msg: 
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg
        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recv")
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = ''
    