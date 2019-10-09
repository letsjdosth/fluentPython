#v4 목표: 해시가능하게 만들기

from array import array
import reprlib
import math
import numbers
import functools
import operator

class Vector:
	typecode='d'
	shortcut_names='xyzt'

	def __init__(self, components):
		self._components=array(self.typecode, components)

	def __iter__(self):
		return iter(self._components)

	def __repr__(self):
		components=reprlib.repr(self._components)
		components=components[components.find('['):-1]
		return 'Vector({})'.format(components)

	def __str__(self):
		return str(tuple(self))

	def __bytes__(self):
		return (bytes([ord(self.typecode)])+bytes(self._components))

	def __eq__(self,other):
		#기존 
		# return tuple(self)==tuple(other) #<-tuple이 커지면 비효율적이게 될 수 있음. 통째로 한번에 만들어 비교해야하기 때문
		
		#개선1
		# if len(self)!=len(other):
		# 	return False
		# for a,b in zip(self,other): 
		# #zip(x,y): 각 반복형에서 나온 항목들을 tuple로 반환하는 제너레이터를 만든다. 병렬 반복 
		# #zip은 길이가 다르면 문제가 생길 수 있음(짧은쪽에 맞추어 걍 중단함). 사용 시 위에 꼭 len 검사를 할 것
		# 	if a!=b:
		# 		return False
		# return True

		#개선2
		return len(self)==len(other) and all(a==b for a, b in zip(self,other)) 
		#all은 정확히 위의 for문의 로직을 사용한다
		#zip()이 중간에 멈추지 않는지 체크해야 하는것은 동일하기 때문에 len 검사를 해야 한다


	def __hash__(self): #<-__eq__ 가까이에 두자 #xor 비트연산을 모든 요소의 해시에 반복적용해 객체의 해시값을 만들어보자
		hashes=(hash(x) for x in self._components) #==map(hash, self_components)
		return functools.reduce(operator.xor, hashes, 0) #reduce(function, iterable object, initial value)
		#참고: initial value는 iterable object가 비어있을 때 기본 반환값으로도 사용됨. 그러니 함수의 '항등원'을 사용할 것

	def __abs__(self):
		return math.sqrt(sum(x*x for x in self))

	def __bool__(self):
		return bool(abs(self))

	@classmethod
	def frombytes(cls, octets):
		typecode=chr(octets[0])
		memv=memoryview(octets[1:]).cast(typecode)
		return cls(memv)

	def __len__(self):
		return len(self._components)

	def __getitem__(self,index):
		cls=type(self)
		if isinstance(index, slice):
			return cls(self._components[index])
		elif isinstance(index, numbers.Integral):
			return self._components[index]
		else:
			msg='{cls.__name__} indices must be integers'
			raise TypeError(msg.format(cls=cls))

	def __getattr__(self,name):
		cls=type(self)
		if len(name)==1:
			pos=cls.shortcut_names.find(name)
			if 0<=pos<len(self._components):
				return self._components[pos]
		msg='{.__name__!r} object has no attribute {!r}'
		raise AttributeError(msg.format(cls, name))

	def __setattr__(self,name,value):
		cls=type(self)
		if len(name)==1:
			if name in cls.shortcut_names:
				error='read-only attribute {attr_name!r}'
			elif name.islower():
				error="can't set attribute 'a' to 'z' in {cls_name!r}"
			else:
				error=''
			if error:
				msg=error.format(cls_name=cls.__name__, attr_name=name)
				raise AttributeError(msg)
		super().__setattr__(name,value)


#v1 test
assert repr(Vector([3.1, 4.2]))=='Vector([3.1, 4.2])'
assert repr(Vector((3,4,5)))=='Vector([3.0, 4.0, 5.0])'
assert repr(Vector(range(10)))=='Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])'

#v2 test
v1=Vector([3,4,5])
assert len(v1)==3
assert v1[0],v1[-1]==(3.0, 5.0)
v7=Vector(range(7))
# assert repr(v7[1:4])=="array('d', [1.0, 2.0, 3.0])" #<-맘에 안든다
assert repr(v7[1:4])=="Vector([1.0, 2.0, 3.0])"
try:
	v7[1,2]
	raise AssertionError
except TypeError as e:
	pass

#v3 test
v10=Vector(range(10))
assert v10.x==0.0
assert (v10.y, v10.z, v10.t)==(1.0, 2.0, 3.0)
try:
	print(v10.p)
	raise AssertionError
except AttributeError as e:
	pass
try:
	v10.x=10
	raise AssertionError
except AttributeError as e:
	pass

#v4 test
print(hash(Vector([3.1,4.2,5.3,6.4,7.5])))