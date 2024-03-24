import machine
import binascii

mac = binascii.hexlify(machine.unique_id()).decode('utf-8')
print(mac)

