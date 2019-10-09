class StrKeyDict0(dict):
	def __missing__(self,key): #key가 존재하지 않을 때 호출됨
		if isinstance(key,str):
			raise KeyError(key)
		return self[str(key)]

	def get(self,key,default=None):
		try:
			return self[key]
		except KeyError:
			return default

	def __contains__(self,key):
		return key in self.keys() or str(key) in self.keys()


#for test

d=StrKeyDict0([('2','two'),('4','four')])

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
