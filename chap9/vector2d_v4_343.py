#목표: 메모리 사용량 개선
#기본적으로 attribute는 __dict__라는 dict에 저장. dictionary는 해시테이블을 사용하므로 빠르지만, 공간을 많이 먹음
#__slots__을 사용하면, dict 대신 다른 콜렉션에 저장하도록 할 수 있음.
#예로, tuple에 저장하면 메모리 사용량이 훨씬 개선됨. 추가적으로 불변형을 강요할 수 있음(tuple은 변경이 안되기 때문에)


from array import array
import math

class Vector2d:
	typecode='d'
	__slots__=('__x','__y') #<-slots 추가. 튜플로 만들자. 그러면 인터프리터는 속성들을 __dict__ 대신 튜플에 저장한다.
	#주의! __slots__를 사용하는 경우, 객체는 __slots__에 명시되지 않은 속성을 가질 수 없게 됨. 그러니 모든 사용하는 내부 속성을 명시할 것
	#주의! __slots__에 __dict__를 넣지 말 것. 이러면 다시 동적으로 속성 할당을 할 수 있게 되지만, 해당 동적 속성은 __dict__에 저장되어 __slots__의 효과를 반감시킨다
	#주의! 약한 참조 사용 시 __weakref__을 __slots__에 추가할 것. (없으면 해당 객체에 대한 약한참조가 막힌다)
	#주의! __slots__는 상속되지 않음. 자식 클래스에서도 따로 명시적으로 다시 설정해주어야 한다.

	def __init__(self,x,y):
		self.__x=float(x)
		self.__y=float(y)

	@property
	def x(self):
		return self.__x

	@property
	def y(self):
		return self.__y

	def __iter__(self):
		return (i for i in (self.x, self.y))

	def __repr__(self):
		class_name=type(self).__name__
		return '{}({!r}, {!r})'.format(class_name,*self) 

	def __str__(self):
		return str(tuple(self))

	def __bytes__(self):
		return bytes([ord(self.typecode)])+bytes(array(self.typecode,self)) 
		
	def __eq__(self,other):
		return tuple(self)==tuple(other)

	def __abs__(self):
		return math.hypot(self.x,self.y)

	def __bool__(self):
		return bool(abs(self))

	@classmethod
	def frombytes(cls,octets):
		typecode=chr(octets[0])
		memv=memoryview(octets[1:]).cast(typecode)
		return cls(*memv)

	def angle(self):
		return math.atan2(self.y, self.x)

	def __format__(self, fmt_spec=''):
		if fmt_spec.endswith('p'):
			fmt_spec=fmt_spec[:-1]
			coord=(abs(self),self.angle())
			outer_fmt='<{}, {}>'
		else:
			coord=self 
			outer_fmt='({}, {})'
		components=(format(c, fmt_spec) for c in coord)
		return outer_fmt.format(*components)

	def __hash__(self):
		return hash(self.x)^hash(self.y)

#test
if __name__=='__main__':
	v1=Vector2d(3,5)
	print(dir(v1))
	try:
		print(v1.__dict__)
	except AttributeError as e:
		print('AttributeError: ',e)