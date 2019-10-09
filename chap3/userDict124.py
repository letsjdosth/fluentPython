import collections

class StrKeyDict(collections.UserDict):
	def __missing__(self,key):
		if isinstance(key,str):
			raise KeyError(key)
		return self[str(key)]

	def __contains__(self,key):
		return str(key) in self.data

	def __setitem__(self,key,item):
		self.data[str(key)]=item


#for test

d=StrKeyDict([('2','two'),('4','four')])

assert d['2']=='two'
assert d[4]=='four'
try:
	d[1]
	raise AssertionError
except KeyError:
	pass
assert d.get('2')=='two'
assert d.get(4)=='four'
assert d.get(1,'N/A')=='N/A'
assert 2 in d
assert 1 not in d

print(d.data)
print(2 in d.data)
print('2' in d.data)