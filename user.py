#!/usr/bin/env python

import socket
from operators import *
from errors import *
import packet

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#Ethan adding stuff for user input
print ("Please enter an operation, operand1, and operand2")
op = input('Choose an operation')
opr1 = float(input('Choose first operand'))
opr2 = float(input('Choose second operand'))
print ("op: ",op," opr1: ",opr1," opr2: ",opr2)
if op == '+':
    op = ADD
elif op == '-':
    op = SUB
elif op == '*':
    op = MUL
elif op == '/':
    op = DIV
#End Ethan stuff
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#Request Packet
rp = packet.RequestPacket(op)
s.send(rp.pack())
#End Request packet
verf = s.recv(20)
vcp = packet.VerifyComputePacket.unpack(verf)
goahead = vcp.get_response()
if goahead == YES:
# Data Compute Packet
    dcp = packet.DCPacket(op, opr1, opr2)
    s.send(dcp.pack())
    # End Data Compute Packet

    ans = s.recv(20)
    rcp = packet.RCPacket.unpack(ans)
    result = rcp.get_result()
    error = rcp.get_error()
    print(error)

    if error == NO:
        print("Answer =", result)
    elif error == ZERO:
        print("Divided by zero error")
    elif error == OTHER:
        print("Unknown error occurred")



s.close()
