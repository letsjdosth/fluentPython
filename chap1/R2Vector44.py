from math import hypot

class Vector:
	def __init__(self,x=0,y=0):
		self.x=x
		self.y=y

	def __repr__(self):
		return 'Vector(%r,%r)'%(self.x, self.y)

	def __abs__(self):
		return hypot(self.x,self.y)

	def __bool__(self):
		return bool(abs(self)) #abs(self)가 0이면 False, 나머지 True
		#return bool(self.x or self.y) #fast version

	def __add__(self, other):
		x=self.x+other.x
		y=self.y+other.y
		return Vector(x,y)

	def __mul__(self,scalar):
		return Vector(self.x*scalar, self.y*scalar)

test=Vector(1,1)
print(test)

print(Vector(2,4)+Vector(2,1))
print(Vector(1,3)*2)
# print(5*Vector(2,2)) #error. 순서 뒤바꾼 경우를 위해 __rmul__을 정의
print(abs(Vector(3,4)))
print(bool(Vector(0,0)),bool(Vector(1,0)))