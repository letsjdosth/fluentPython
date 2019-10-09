#다차원 벡터 사용자 정의 시퀀스 Vector 설계
#목표:
# Vector2d와 최대한 호환
# 반복형을 인수로 받도록 (내장 시퀀스처럼)

from array import array
import reprlib
import math

class Vector:
	typecode='d'

	def __init__(self, components):
		self._components=array(self.typecode, components) #<-그냥 array로 저장함

	def __iter__(self):
		return iter(self._components) #array의 반복자를 그대로 돌려주자

	def __repr__(self):
		components=reprlib.repr(self._components) #array의 repr를 부른다. 
		#참고: reprlib.repr는 생성 문자열의 길이를 제한하고 ...로 치환한다. 대형 구조체/재귀적 구조체 출력 시 유용
		#참고: repr(array('d',[1,2,3,4,5])) 출력: 'array('d', [1.0, 2.0, 3.0, 4.0, 5.0])'
		components=components[components.find('['):-1] #array의 데이터 부분(즉 [] 사이)만 가져온다
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
		return cls(memv) #<-이제 튜플 언패킹을 안 하고 그대로 넘겨도 된다. 2d버전과 달리 반복형을 그냥 받기 때문


#for test
assert repr(Vector([3.1, 4.2]))=='Vector([3.1, 4.2])'
assert repr(Vector((3,4,5)))=='Vector([3.0, 4.0, 5.0])'
assert repr(Vector(range(10)))=='Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])'

