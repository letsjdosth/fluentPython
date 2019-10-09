from types import MappingProxyType

d={1:'A'}
d_proxy=MappingProxyType(d)
print(d_proxy)
print(d_proxy[1])
try:
	d_proxy[2]='x' #TypeError: 'mappingproxy' object does not support item assignment
	raise AssertionError
except TypeError:
	pass

d[2]='B'
print(d_proxy) #계속 d를 보고있다! '동적 뷰'
print(d_proxy[2])