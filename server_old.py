#!/usr/bin/env python
import socket
import random

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20

s = socket.socket()
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
while True:
    
    data = conn.recv(BUFFER_SIZE)
    
    if not data: break
    print ('received data:', data)
    #Ethan adding stuff for return packet
    chance = random.randint(0,99)
    print('random chance: ', chance)
    if chance < 89:
        data = b'0001'
    else:
        data = b'0000'
    #Ethan end return packet stuff
    conn.send(data)  # echo
conn.close()
