import struct

with open('filter.gif','rb') as fp:
	img=memoryview(fp.read()) #mmap(메모리맵)이 더 적은 바이트로 복사되긴 함

header=img[:10]

print(bytes(header))
#b'GIF89aq\x02X\x02'

fmt='<3s3sHH' #<:little endian, 3s: 3byte sequence, H:int of hex(16)
print(struct.unpack(fmt,header))
#(b'GIF', b'89a', 625, 600) #GIF파일의 첫 10바이트는 종류,버전,너비,높이임. 해당하는 대로 fmt를 통해 자른 것

del header
del img