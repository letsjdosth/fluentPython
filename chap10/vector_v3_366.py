#v3 목표: 앞에 요소 몇개는 x,y,z,t 등 속성 이름으로 접근할 수 있도록 하자

from array import array
import reprlib
import math
import numbers

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
		return len(self._components)

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

	def __getattr__(self,name): #<-self.x 형태로 부르면 이름 찾기 규칙에 따라 객체속성-클래스속성-상속그래프따라 올라가며 찾은 속성-이후 __getattr_를 부른다. x가 name자리로 들어옴
		cls=type(self)
		if len(name)==1:
			pos=cls.shortcut_names.find(name)
			if 0<=pos<len(self._components):
				return self._components[pos]
		msg='{.__name__!r} object has no attribute {!r}' #<-나중에 할일: 1. 포맷언어 인수이름자리에 .붙여서 부르면 뭐가 되는건지? 2. 뒤에 !r붙이면 repr를 호출?
		raise AttributeError(msg.format(cls, name))

	def __setattr__(self,name,value): #<-self.x=y 형태로 할당문이 나오면 __setattr__의 name자리에 x, value자리에 y가 들어온다
		cls=type(self)
		if len(name)==1:
			if name in cls.shortcut_names:
				error='read-only attribute {attr_name!r}'
			elif name.islower():
				error="can't set attribute 'a' to 'z' in {cls_name!r}" #<-단 이렇게 막으면 모든 단일 소문자 속성이 막혀버린다(다른 용도로 쓸래도..)
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
	raise AssertionError #<-x,y,z,t로 접근해 할당하는건 막아버리자
except AttributeError as e:
	pass
