import uctypes

COORD = {
    "x": 0 | uctypes.UINT16,
    "y": 2 | uctypes.UINT16,
}

STRUCT = {
    "data1": 0 | uctypes.UINT8,
    "data2": 1 | uctypes.UINT8,
    "data3": (2, COORD),
    "data4": 7| 0<<uctypes.BF_POS | 4<<uctypes.BF_LEN | uctypes.BFUINT8
}

buf = bytearray(8)
datastruct = uctypes.struct(uctypes.addressof(buf), STRUCT)
datastruct.data1 = 1
datastruct.data2 = 2
datastruct.data3.x = 65535
datastruct.data3.y = 7691
datastruct.data4 = 5

print("buf:", buf)
print("data1:", datastruct.data1)
print("data2:", datastruct.data2)
print("data3.x:", datastruct.data3.x)
print("data3.y:", datastruct.data3.y)
print("data4:", datastruct.data4)

size = uctypes.sizeof(datastruct)
print("size:", size)

address = uctypes.addressof(datastruct)
print("address:", hex(address))
print("bytes_at:", uctypes.bytes_at(address, size))
print("bytearray_at:", uctypes.bytearray_at(address, size))
