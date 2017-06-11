import struct

operator = b'+'
operand1 = 42
operand2 = 144

fmt = 'cqq'

data = struct.pack(fmt, operator, operand1, operand2)
print(data)

tuple_data = struct.unpack(fmt, data)
print(tuple_data)
