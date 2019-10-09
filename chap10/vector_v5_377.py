#v5 목표: 포맷팅으로 구면좌표계 구현

from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools

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
		return len(self)==len(other) and all(a==b for a, b in zip(self,other)) 

	def __hash__(self):
		hashes=(hash(x) for x in self._components)
		return functools.reduce(operator.xor, hashes, 0)

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

	def angle(self,n):
		r=math.sqrt(sum(x*x for x in self[n:]))
		a=math.atan2(r,self[n-1])
		if (n==len(self)-1) and (self[-1]<0):
			return math.pi*2-a
		else:
			return a

	def angles(self):
		return (self.angle(n) for n in range(1, len(self)))

	def __format__(self,fmt_spec=''):
		if fmt_spec.endswith('h'): #h가 들어오면 초구면좌표로 바꾼다
			fmt_spec=fmt_spec[:-1]
			coords=itertools.chain([abs(self)],self.angles())
			#itertools.chain(*iterables)
			#Make an iterator that returns elements from the first iterable until it is exhausted, then proceeds to the next iterable, until all of the iterables are exhausted. 
			#Used for treating consecutive sequences as a single sequence.
			#즉, 위 코드는 [abs(self)],이후 angles의 요소를 하나씩 반환하는 순회가능한 제너레이터를 만든다
			outer_fmt='<{}>'
		else:
			coords=self
			outer_fmt='({})'
		components=(format(c, fmt_spec) for c in coords)
		return outer_fmt.format(', '.join(components))


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

#v5 test
v2dim=Vector([3,4])
assert format(v2dim)=='(3.0, 4.0)'
assert format(v2dim,'.2f')=='(3.00, 4.00)'
assert format(v2dim,'.3e')=='(3.000e+00, 4.000e+00)'
print(format(v2dim,'h'))
print(format(Vector([1,1,1]),'.3eh'))
print(format(Vector([1,1,1,1]),'0.5fh'))
