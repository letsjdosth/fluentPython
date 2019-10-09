from array import array
import math

class Vector2d:
	typecode='d' #<-Vector2d와 bytes간 변환 시 사용 #array.array에서 'd'는 C의 double, python의 8byte float에 대응

	def __init__(self,x,y):
		self.x=float(x)
		self.y=float(y)

	def __iter__(self): #<-iterable한 객체로 만듬. (tuple unpacking시 __iter__를 부름)
		return (i for i in (self.x, self.y)) #<-generator expression

	def __repr__(self):
		class_name=type(self).__name__ #<-직접 클래스 이름을 쓰지 않고 __name__을 가져온다. 이는 나중에 이 클래스를 상속 시에도 안전하게 쓸 수 있도록 하기 위함
		return '{}({!r}, {!r})'.format(class_name,*self) 
		# {!r}: format에 전달되는 각 요소에 repr()을 호출하여 반환된 값을 문자열로 치환해 넣는다. 
		#*self는 __iter__를 불러 만든 튜플이 된다. 즉, (self.x, self.y) 가 된다.

	def __str__(self):
		return str(tuple(self)) #<-__iter__가 있으므로 간단히 (self.x, self.y)가 된다.

	def __bytes__(self):
		return bytes([ord(self.typecode)])+bytes(array(self.typecode,self)) 
		#ord(c)
		#하나의 유니코드 문자를 나타내는 문자열이 주어지면 해당 문자의 유니코드 코드 포인트를 나타내는 정수를 돌려줍니다. 
		#예를 들어, ord('a') 는 정수 97 을 반환하고 ord('€') (유로 기호)는 8364 를 반환합니다.
		#array.array(typecode[,initializer])
		#A new array whose items are restricted by typecode, and initialized from the optional initializer value, 
		#which must be a list, a bytes-like object, or iterable over elements of the appropriate type.
		#따라서 위 코드는, 타입코드('d')에 해당하는 유니코드 코드 포인트를 바이트형으로 앞에 하나 붙이고, 이후 self의 bytes 변환값을 double형 array에 넣게 됨

	def __eq__(self,other):
		return tuple(self)==tuple(other)

	def __abs__(self):
		return math.hypot(self.x,self.y)

	def __bool__(self):
		return bool(abs(self))


#for test
v1=Vector2d(3,4)
print(v1.x, v1.y) #<-attribute 직접접근

x,y=v1 #<-tuple 언패킹
print(x,y)

print(repr(v1)) #Vector2d(3.0, 4.0) #<-repr()는 소스코드를 출력. __repr__() 정의 #참고: 콘솔에선 v1 으로 부르면 repr()호출
v1_clone=eval(repr(v1))
assert v1==v1_clone #<-repr() 출력과 더불어, ==를 오버라이딩

print(v1) #(3.0, 4.0) #<- 순서쌍 출력. __str__을 정의
octets=bytes(v1) #<-이진표현 생성. __bytes__() 정의
print(octets) 

print(abs(v1)) #5.0 #<-__abs__ 정의
print(bool(v1), bool(Vector2d(0,0))) #True, False #<-__bool__ 정의. 크키가 0이면 False, 아니면 True 반환


