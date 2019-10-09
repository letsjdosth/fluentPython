#개선 목표: 해시가능하게 하자
from vector2d_v2_332 import Vector2d as Vector2d_v2
v1=Vector2d_v2(3,4)
try:
	hash(v1)
except TypeError as e:
	print(e) #unhashable type: 'Vector2d'
#때문에 set 등에 집어넣을 수 없음
#해시가능하게 하려면 __hash__와 __eq__를 구현하면 된다. __eq__는 이미 있으므로, __hash___만 구현하자

#또한, __hash__를 구현하기 위해, 불변형으로 만들자. 
#이유: 아래에서 해시값 설정 시 어트리뷰트값을 사용하는데, 나중에 어트리뷰트값이 변하면 재계산한 객체 해시값이 변해서 이는
#객체 수명주기동안 해시값이 같아야한다는 조건을 건드리기 때문
#- 어트리뷰트값을 사용해 해시값을 만들지 않는다면, 굳이 불변형으로 만들 필요는 없다. __hash__, __eq__만 나름의 방식으로 제대로 구현하면 됨
#- 하지만 ==의 조건으로 객체 내부 평가 시 어트리뷰트값을 이용한다면, 다른 어트리뷰트 값에 의해 hash값을 다르게/같은 어트리뷰트 값에 의해 hash값을 같게 만들어야 하고,
#  따라서 해시값이 어트리뷰트값의 함수가 된다. 하지만 해시값은 객체 수명주기간 바뀌면 안 되므로, 이는어트리뷰트값이 객체수명주기간 불변해야 한다(=객체는 불변형이어야 한다)는 제약을 걸어야만 한다.)

from array import array
import math

class Vector2d:
	typecode='d'

	def __init__(self,x,y):
		self.__x=float(x) #<-불변형 작업: x,y를 비공개 속성으로 만들자 (완벽히 비공개는 아님)
		self.__y=float(y)

	@property #<-getter
	def x(self):
		return self.__x

	@property #<-getter
	def y(self):
		return self.__y
	#불변형 작업: getter만 만들고 setter는 만들지 말자

	def __iter__(self):
		return (i for i in (self.x, self.y)) #<-x,y를 읽기만 하는 나머지 부분에서는 그냥 써도 문제가 없다

	def __repr__(self):
		class_name=type(self).__name__
		return '{}({!r}, {!r})'.format(class_name,*self) 

	def __str__(self):
		return str(tuple(self))

	def __bytes__(self):
		return bytes([ord(self.typecode)])+bytes(array(self.typecode,self)) 
		
	def __eq__(self,other): #<-이미 있다
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
		#목표
		#1. int형 반환
		#2. 동일한 객체는 동일 해시값을 가져야 한다. (__eq__와 연계)
		#공식 문서에서 추천하는 방식은 어트리뷰트의 해시의 비트단위에 XOR(연산자 ^)을 사용하는 것. 이를 따라보자
		return hash(self.x)^hash(self.y)

#test
if __name__=='__main__':
	v1=Vector2d(3, 4)
	v2=Vector2d(3.1, 4.2)
	print(hash(v1),hash(v2)) #7 384307168202284039 #<-다른 값은 다른 해시값이 나온다
	print(set([v1,v2])) #<-이제 set에 잘 들어간다
	v3=Vector2d(3, 4)
	print(hash(v3)) #7 #<-같은 값은 같은 해시값이 나온다
	print(v1==v3) #True #<-값이 같다
	print(v1 is v3) #False #주의! 해시값이 같다는 소리는 값이 같다는 소리이지 (dict에서 검색용으로 쓰기 위해 해시 테이블을 쓴다는 것을 기억!), 메모리 주소가 같단 소리가 아니다
