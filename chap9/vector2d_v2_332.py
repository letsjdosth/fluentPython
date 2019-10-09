#개선 목표: format을 지원하자

from array import array
import math

class Vector2d:
	typecode='d'

	def __init__(self,x,y):
		self.x=float(x)
		self.y=float(y)

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

	def angle(self): #<-__format__에서 극좌표 리턴을 구현하기 위해 새로운 메소드를 만든다
		return math.atan2(self.y, self.x) #math.atan2(y,x): Return atan(y / x), in radians. (tangent(rad)=y/x 이므로 이의 역함수임)

	def __format__(self, fmt_spec=''): #<-{:format_spec} 치환필드를 파싱한다 format330.py 참고
		if fmt_spec.endswith('p'):
		#주의. 사용자 포맷코드는 기존 포맷코드와 헷갈리게 쓰지 말 것. 물론 타입에 따라 돌아가므로 겹쳐도 에러가 나진 않지만, 사용자가 괴로움.
		#이미 쓰고있는 코드: 정수형 bcdoxXn 실수형 eEfFgGn%, 문자형 s
			fmt_spec=fmt_spec[:-1]
			coord=(abs(self),self.angle())
			outer_fmt='<{}, {}>'
		else:
			coord=self 
			outer_fmt='({}, {})'
		components=(format(c, fmt_spec) for c in coord) #<-각각을 format에 넣고 (float가 들어있으므로 float 규칙을 가져가게 된다) #__iter__가 구현되어 있다!
		return outer_fmt.format(*components) #<-출력 문자열


##for test
v1=Vector2d(3,4)
v2=Vector2d(1,1)

#float 형식 지원
assert format(v1)=='(3.0, 4.0)'
assert format(v1,'.2f')=='(3.00, 4.00)'
assert format(v1,'.3e')=='(3.000e+00, 4.000e+00)'

#임의 포맷코드 지원
#포맷 명시자가 p로 끝나면 벡터를 극좌표로 리턴
assert format(v2,'p')=='<1.4142135623730951, 0.7853981633974483>'
assert format(v2,'.3ep')=='<1.414e+00, 7.854e-01>'
assert format(v2,'0.5fp')=='<1.41421, 0.78540>'