#!/usr/bin/env python
import struct
from operators import *
from errors import *

DCP_FORMAT = '>cdd'
RCP_FORMAT = '>cd'
REQUEST_FORMAT ='>c'

class Packet(object):
    
    def __init__(self, fmt, *data):
        self.fmt = fmt
        self.data = data
    
    def pack(self):
        return struct.pack(self.fmt, *self.data)
    


class DCPacket(Packet):
    
    def __init__(self, operator, *operands):
        super(DCPacket, self).__init__(DCP_FORMAT, operator, *operands)
        self.operator = operator
        if operator == ADD or operator == SUB   \
            or operator == MUL or operator == DIV:
            self.operand1 = operands[0]
            self.operand2 = operands[1]

    def get_operator(self):
        return self.operator
    
    def get_operands(self):
        if self.operator == ADD or self.operator == SUB   \
            or self.operator == MUL or self.operator == DIV:
            return (self.operand1, self.operand2)
        return None
    
    @staticmethod
    def unpack(byte_string):
        print(byte_string)
        data = struct.unpack(DCP_FORMAT, byte_string)
        if data[0] == ADD or data[0] == SUB   \
            or data[0] == MUL or data[0] == DIV:
            return DCPacket(data[0], data[1], data[2])
        return None

class RCPacket(Packet):
    
    def __init__(self, error, result):
        super(RCPacket, self).__init__(RCP_FORMAT, error, result)
        self.result = result
        if error == NO or error == ZERO   \
            or error == OTHER:
            self.error = error
               
    def get_result(self):
        return self.result
    
    def get_error(self):
        return self.error

    def unpack(byte_string):
        print(byte_string)
        data = struct.unpack(RCP_FORMAT, byte_string)
        return RCPacket(data[0], data[1])
        
class RequestPacket(Packet):
    
    def __init__(self, operator):
        super(RequestPacket, self).__init__(REQUEST_FORMAT,operator)
        self.operator = operator
        
    def get_op(self):
        return self.operator
        
    def unpack(byte_string):
        print(byte_string)
        data = struct.unpack(REQUEST_FORMAT, byte_string)
        return RequestPacket(data[0])
        
class VerifyComputePacket(Packet):

    def __init__(self, response):
        super(VerifyComputePacket, self).__init__(REQUEST_FORMAT,response)
        self.response = response
    
    def get_response(self):
        return self.response

    def unpack(byte_string):
        print(byte_string)
        data = struct.unpack(REQUEST_FORMAT, byte_string)
        return VerifyComputePacket(data[0])
