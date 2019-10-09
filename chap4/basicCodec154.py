for codec in ['latin_1','utf_8','utf_16']:
	print(codec, 'El Niño'.encode(codec),sep='\t')


#encode
city='São Paulo'
print(city.encode('utf_8'),city.encode('utf_16'),city.encode('iso8859_1'),sep='\n')

try:
	city.encode('cp437') #errors='strict'
	raise AssertionError
except UnicodeEncodeError:
	pass
print(city.encode('cp437',errors='ignore')) #(not recommend)
print(city.encode('cp437',errors='replace')) #replace chars that cannot encode with ? 
print(city.encode('cp437',errors='xmlcharrefreplace')) #replace chars above with XML object


#decode
octets=b'Montr\xe9al' #Montréal
print(octets.decode('cp1252')) #Montréal
print(octets.decode('iso8859_7')) #Montrιal #그리스어 코덱
print(octets.decode('koi8_r')) #MontrИal #러시아어 코덱

try:
	print(octets.decode('utf_8')) #걍 에러남
	raise AssertionError
except UnicodeDecodeError:
	pass
print(octets.decode('utf_8',errors='replace')) #�(U+FFFD, REPLACEMENT CHARACTER(유니코드 공식 치환 문자))로 치환함.

