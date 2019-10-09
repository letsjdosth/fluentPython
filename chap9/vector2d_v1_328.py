#개선 목표: bytes에서 다시 원래 인스턴스로 돌려놓을 수 있도록 하자

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

	#want: __bytes__로 만든 bytes표현을 다시 원래 클래스로 돌리는 메소드
	@classmethod #<-인스턴스가 없을때도 바로 작동해 인스턴스를 돌려줄 수 있도록(일종의 대안 생성자) classmethod로 구현한다. 데커레이터를 붙이자
	def frombytes(cls,octets): #<-self가 아니라 cls로 자기자신을 전달한다
		typecode=chr(octets[0]) #<-첫바이트는 typecode(__bytes__에서 그렇게 만들었기 때문)
		memv=memoryview(octets[1:]).cast(typecode) #<-데이터부분 형변환
		return cls(*memv)

#for test
octet=b'd\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
recovered=Vector2d.frombytes(octet)
print(recovered) #(3.0, 4.0)