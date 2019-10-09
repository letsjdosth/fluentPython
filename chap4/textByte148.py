#encode(codepoint->bytes) & decode(bytes->codeopoint)
s='café'
print(s,len(s)) #4. 4글자

b=s.encode('utf8')
print(b,len(b)) #5. 5바이트로 인코딩되었기 때문

d=b.decode('utf8')
print(d, len(d))

#bytearray
cafe=bytes('café',encoding='utf-8')
print(cafe)
print(cafe[0],cafe[:1])

cafe_arr=bytearray(cafe)
print(cafe_arr,cafe_arr[-1:])


#making bytes or bytearray
print('café'.encode('utf8'))
print(bytes([1,255,24,36]))
print(bytes.fromhex('31 4B CE A9'))

import array
numbers=array.array('h',[-2,-1,0,1,2]) #h: short int (2byte)
octets=bytes(numbers)
print(octets, len(octets)) #10 byte
#in addition, bytes(),byteviews(),memoryview...