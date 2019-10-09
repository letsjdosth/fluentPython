#v8 목표: 연산자 오버로딩. 
#'향상된 비교 연산자' (==,!=,>,<.>=,<=)
# 몇몇 복합할당 연산자 (+=,*=) (불변형 객체)

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
		if isinstance(other, Vector): #<-보수적 접근으로, 컨테이너의 자료형 검사를 하자
			return len(self)==len(other) and all(a==b for a, b in zip(self,other)) 
		else:
			return NotImplemented

	def __hash__(self):
		hashes=(hash(x) for x in self._components)
		return functools.reduce(operator.xor, hashes, 0)

	def __abs__(self):
		return math.sqrt(sum(x*x for x in self))

	def __bool__(self):
		return bool(abs(self))

	def __neg__(self):
		return Vector(-x for x in self)

	def __pos__(self):
		return Vector(self)

	def __add__(self,other):
		try:
			pairs=itertools.zip_longest(self,other,fillvalue=0.0)
			return Vector(a+b for a,b in pairs)
		except TypeError:
			return NotImplemented

	def __radd__(self,other):
		return self+other

	def __mul__(self,scalar):
		if isinstance(scalar, numbers.Real):
			return Vector(n*scalar for n in self)
		else:
			return NotImplemented

	def __rmul__(self,scalar):
		return self*scalar

	def __matmul__(self,other):
		try:
			return sum(a*b for a,b in zip(self, other))
		except TypeError:
			return NotImplemented

	def __rmatmul__(self,other):
		return self@other



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

#v6 test
assert -v2dim==Vector([-3,-4])
assert +v2dim==v2dim
v2=Vector([6,7,8])
assert v1+v2==Vector([3+6, 4+7, 5+8])
v3=Vector([3,4,5,6])
v4=Vector([1,2])
assert v3+v4==Vector([3+1,4+2,5+0,6+0])

from vector2d_v3_334 import Vector2d
v2d=Vector2d(1,2)
assert v1+v2d==Vector([4,6,5])
assert v2d+v1==Vector([4,6,5])

#v7 test
assert v1*10==Vector([3*10,4*10,5*10])
assert 11*v1==Vector([3*11,4*11,5*11])
from fractions import Fraction
print(v1*Fraction(1,3))
assert v1@v2==3*6+4*7+5*8


#v8 test
#__eq__: 기존 return len(self)==len(other) and all(a==b for a, b in zip(self,other)) 
va=Vector([1.0,2.0,3.0])
vb=Vector(range(1,4))
vc=Vector([1,2])
assert va==vb
assert vc==v2d #<-기존에도 같다고 한다. 왜냐면 Vector가 NotImplemented를 반환해도, 이후 역순 차례에서 Vector2d(v3)에서 tuple로 바꿔 비교하기 때문
t3=(1,2,3)
assert not va==t3 #<기존에는 같다고 한다. __iter__로 하나씩 떼서 검사하므로, 둘다 순회가능하므로 컨테이너의 자료형과는 상관없기 때문

#__ne__ <-따로 구현 안 하면 not(a==b)를 반환한다
assert not va!=vb
assert not vc!=v2d
assert va!=t3

#복합 할당 연산자
#+=, *=는 __iadd__, __imul__을 구현하지 않아도 이미 동작한다. __i~__가 없으면 인터프리터가 +, *을 가지고 알아서 작동시키기 때문 (a+=b -> a=a+b)
v1=Vector([1,2,3])
v1_alias=v1 #2841183743000
print(id(v1))
v1+=Vector([4,5,6]) #<-동작한다
print(v1) #(5.0, 7.0, 9.0) #<-결과도 예상과 같다
print(id(v1)) #2841185369224 #<-달라졌다! + 연산자에서 객체를 변경하는 것이 아니라 새로 만들어 반환하기 때문
print(v1_alias) #(1.0, 2.0, 3.0) #<-기존 객체는 그대로 있다. v1을 새로 만들어 재바인딩했다는 것의 또다른 증거이다

v1*=11 #<-동작한다
print(v1) #(55.0, 77.0, 99.0) #<-결과 역시 예상과 같다
print(id(v1)) #2277682049656 #<-또 바뀐다. +와 마찬가지로 *도 새 객체를 만들어 바인딩하기 때문

#참고로, __i~__ method (inplace method)는 새 객체를 만드는 것이 아니라 기존 객체를 변경하는 방식으로 짜는 것이 일반적임
#때문에 불변 객체에서는 인플레이스 메소드를 구현하지 '말 것'