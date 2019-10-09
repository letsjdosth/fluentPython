"""RC4 호환 알고리즘 (RC4 암호화 알고리즘 파이썬 구현)"""

def arcfour(key, in_bytes, loops=20):
	kbox=bytearray(256) #키박스
	for i, car in enumerate(key):
		kbox[i]=car
	j=len(key)
	for i in range(j, 256): #가득 찰 때까지 반복
		kbox[i]=kbox[i-j]

	#[1] sbox 초기화
	sbox=bytearray(range(256))

	#CipherSaber-2 권고대로 sbox 혼합 루프를 반복
	j=0
	for k in range(loops):
		for i in range(256):
			j=(j+sbox[i]+kbox[i])%256 #<-키가 여기 들어간다
			sbox[i],sbox[j]=sbox[j],sbox[i]

	#main loop
	i=0
	j=0
	out_bytes=bytearray()

	for car in in_bytes:
		i=(i+1)%256
		#[2] sbox 셔플링
		j=(j+sbox[i])%256
		sbox[i],sbox[j]=sbox[j],sbox[i]
		#[3] t 계산
		t=(sbox[i]+sbox[j])%256
		k=sbox[t]
		car=car^k #Bitwise Exclusive Or #<-k를 가지고 in_bytes를 암호화
		out_bytes.append(car)

	return out_bytes

def test():
	from time import time
	clear=bytearray(b'1234567890'*100000)
	t0=time()
	cipher=arcfour(b'key',clear)
	print('elapsed time: %.2fs'%(time()-t0))
	result=arcfour(b'key',cipher)
	assert result==clear, '%r != %r'%(result,clear)
	print('elapsed time: %.2fs'%(time()-t0))
	print('OK')

if __name__=='__main__':
	test()