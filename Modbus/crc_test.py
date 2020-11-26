
crc = ".%4x" % 0x00E4


crc = crc.replace(" ", "0")
print(crc[3:])
print(crc[1:3])
#if crc=="  e4":
print(int(crc[1:3],16))
print(crc)
input()