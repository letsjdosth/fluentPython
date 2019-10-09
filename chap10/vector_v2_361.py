#다차원 벡터 사용자 정의 시퀀스 Vector 설계
#v2 목표:
#시퀀스 프로토콜 구현:
#(__len__, __getitem__ 구현)

from array import array
import reprlib
import math
import numbers

class Vector:
	typecode='d'

	def __init__(self, components):
		self._components=array(self.typecode, components)

	def __iter__(self):
		return iter(self._components)

	def __repr__(self):
		components=reprlib.repr(self._components) #array의 repr를 부른다. 
		components=components[components.find('['):-1]
		return 'Vector({})'.format(components)

	def __str__(self):
		return str(tuple(self))

	def __bytes__(self):
		return (bytes([ord(self.typecode)])+bytes(self._components))

	def __eq__(self,other):
		return tuple(self)==tuple(other)

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
		return len(self._components) #<-array의 len을 돌려주자

	def __getitem__(self,index):
		# return self._components[index] #<-array에 위임하면 코드는 간단하지만, 리턴값이 array 객체가 되어버린다.
		cls=type(self)
		if isinstance(index, slice): #[::]로 접근시 슬라이스 객체 타입으로 들어온다
			return cls(self._components[index]) #<-Vector 생성자가 array를 받을 수 있으므로
		elif isinstance(index, numbers.Integral): #Integral: int의 추상베이스클래스
			return self._components[index]
		else:
			msg='{cls.__name__} indices must be integers'
			raise TypeError(msg.format(cls=cls))


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
