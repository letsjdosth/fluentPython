#Diamond Inheritance 문제
class A:
	def ping(self):
		print('ping:',self)

class B(A):
	def pong(self):
		print('pong:',self)

class C(A):
	def pong(self):
		print('PONG:',self)

class D(B,C):
	def ping(self):
		super().ping()
		print('post-ping:',self)

	def pingpong(self):
		self.ping()
		super().ping()
		self.pong()
		super().pong()
		C.pong(self) #<-C를 명시해 pong을 부른다. 단 이 때는 self를 반드시 명시해서 넘겨야 한다. (객체 메서드를 클래스에서 직접 부르기 때문에 그러함. 바인딩되지 않은 메서드에 접근)

d=D()
d.pong() #pong: <__main__.D object at 0x00000247D3F1DD30> #<-B의 것을 상속해 실행되었다 (C는?!)
C.pong(d) #PONG: <__main__.D object at 0x00000247D3F1DD30> #<-클래스명을 명시하면 해당 클래스의 것이 실행된다

#method resolution order (MRO)
print(D.__mro__) 
#(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
#메소드 이름을 앞에서부터 뒤의 순서로 찾는다. D->B->C->A->object
#MRO의 순서는 상속그래프 뿐 아니라 클래스 선언문(정의)의 영향도 받음. 
# class D(B,C) <B를 먼저 찾는다. D-B-C-A-object
# class D(C,B) <C를 먼저 찾는다. D-C-B-A-object


#super(): 상위 클래스의 메소드 호출
d.pingpong()
#ping: <__main__.D object at 0x00000200C795DCF8> #<-d.ping의 super().ping()은 A의 ping이 된다 (B,C엔 ping()이 없다)
#post-ping: <__main__.D object at 0x00000200C795DCF8>
#ping: <__main__.D object at 0x00000200C795DCF8> #<-d.pingpong의 super().ping()은 A의 ping이 된다
#pong: <__main__.D object at 0x00000200C795DCF8> #<-d.pingpong의 self.pong()은 MRO에 의해 B의 pong이 된다
#pong: <__main__.D object at 0x00000200C795DCF8> #<-d.pingpong의 super().pong()도 MRO에 의해 B의 pong이 된다
#PONG: <__main__.D object at 0x00000200C795DCF8> #<-C를 명시해 부르면 (MRO를 무시하고) C의 것이 실행된다


#추가 예
print(bool.__mro__) #(<class 'bool'>, <class 'int'>, <class 'object'>)
def print_mro(cls):
	print(', '.join(c.__name__ for c in cls.__mro__))
print_mro(bool)

import numbers
print_mro(numbers.Integral) #Integral, Rational, Real, Complex, Number, object

import io
print_mro(io.BytesIO) #BytesIO, _BufferedIOBase, _IOBase, object
print_mro(io.TextIOWrapper) #TextIOWrapper, _TextIOBase, _IOBase, object

import tkinter
print_mro(tkinter.Text) #Text, Widget, BaseWidget, Misc, Pack, Place, Grid, XView, YView, object