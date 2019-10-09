import os

print(os.listdir('.'))
print(os.listdir(b'.'))

print(os.fsencode('digits-of-π.txt')) #os 파일명/경로에서 쓰는 bytes로
print(os.fsdecode('digits-of-π.txt')) #str로


pi_name_bytes=os.listdir(b'.')[4]
# pi_name_str=pi_name_bytes.decode('ascii',errors='surrogateescape')#windows에서는 surrogateescape를 안써서 안되나봄
pi_name_str=pi_name_bytes.decode('utf_8')
print(pi_name_str)

# pi_name_bytes2=pi_name_str.encode('ascii',errors='surrogateescape')
# print(pi_name_bytes2)