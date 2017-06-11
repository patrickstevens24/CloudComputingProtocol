#!/usr/bin/env python

import socket
import threading
import random
import packet
from operators import *
from errors import *

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
TIMEOUT = 0.500     # set the timeout to 500ms
BACKLOG_LIMIT = 4
BUFFER_SIZE = 20

THREAD_ID = 1

class ServerThread(threading.Thread):

    def __init__(self, conn, addr):
        super(ServerThread, self).__init__()
        global THREAD_ID
        self.id = THREAD_ID
        self.conn = conn
        self.client_ip = addr
        THREAD_ID = THREAD_ID + 1

    # Handle comms b/t a client and the server
    def run(self):
        #Request compute packet
        reqData = self.conn.recv(BUFFER_SIZE)
        if not reqData:
            self.report('error receiving data from client, closing thread')
            return
        #print('got request packet')
        rp = packet.RequestPacket.unpack(reqData)
        reqOp = rp.get_op()
        chance = random.randint(0,99)
        if chance <89:
            ver = YES
            #print('can compute')
        else:
            ver = NO
            #print('Can not compute')
        #print('Sending vcp packet')
        vcp = packet.VerifyComputePacket(ver)
        self.conn.send(vcp.pack())
        
        #End Request compute
        if ver==YES:
            # Data Compute Packet
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                self.report('error receiving data from client, closing thread')
                return
            dcp = packet.DCPacket.unpack(data)
            op = dcp.get_operator()
            oprnds = dcp.get_operands()
            self.report('operator:{}, operand1:{}, operand2:{}'
                        .format(op, oprnds[0], oprnds[1]))
            # End Data Compute Packet

            error = NO
            ans = 0.0

            if op == ADD:
                ans = oprnds[0] + oprnds[1]
            elif op == SUB:
                ans = oprnds[0] - oprnds[1]
            elif op == MUL:
                ans = oprnds[0] * oprnds[1]
            elif op == DIV:
                if oprnds[1] == 0:
                    #error
                    error = ZERO
                else:
                    ans = oprnds[0] / oprnds[1]
            else:
                # error
                error = OTHER

            rcp = packet.RCPacket(error, ans)
            self.conn.send(rcp.pack())

    def get_id(self):
        return self.id

    def get_name(self):
        return 'Thread-{}'.format(self.id)

    def to_string(self):
        return '{}, hosting:{}'.format(self.get_name(), self.client_ip)

    def report(self, msg):
        print('{}::\n\t{}'.format(self.to_string(), msg))

def init_server():

    print('Running server on IP={}:{}\n'.format(TCP_IP, TCP_PORT))

    # set up the TCP socket
    sock = socket.socket()
    sock.bind((TCP_IP, TCP_PORT))

    # listen for client connections
    sock.listen(BACKLOG_LIMIT)

    while sock:
        # accept connection from a client
        conn, addr = sock.accept()
        addr = addr[0]
        conn.settimeout(TIMEOUT)
        print('Connection from host on IP={}'.format(addr))

        # create a thread to handle comms w/ client host
        thd = ServerThread(conn, addr)
        print('Server Thread {} created'.format(thd.get_name()))
        thd.start()

    sock.close()
    print('\nListening socket is \'None\', server shutting down!\n')

# run the server
init_server()
