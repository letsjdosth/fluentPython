#간단한 디스크립터 프로토콜을 이용해 프로퍼티 비슷한 것을 객체로 구현하자

class Quantity:
	def __init__(self, storage_name):
		self.storage_name=storage_name
	def __set__(self, instance, value): #<-디스크립터 프로토콜. 관리대상속성에 할당시 __set__을 호출하게 된다.
		if value>0:
			instance.__dict__[self.storage_name]=value #<-인스턴스의 __dict__를 직접 설정해야 한다. setattr을 이용하면 무한재귀호출에 빠진다.
		else:
			raise ValueError('value must be >0')

class LineItem:
	weight=Quantity('weight') #<-클래스 공개속성. (객체속성이 아님. self가 없다) 클래스가 로딩될 때 한번 만들어지고 그걸 모든 LineItem 객체가 함께 쓰게 된다.
	price=Quantity('price') #때문에 line6에서 Quantity의 속성으로 값을 저장하지 않고, LineItem 객체의 __dict__에 저장하는 것이다!
	def __init__(self, description, weight, price):
		self.description=description
		self.weight=weight
		self.price=price
	def subtotal(self):
		return self.weight*self.price

#for test
try:
	truffle=LineItem('White truffle',100,0)
except ValueError as exc:
	print('ValueError:',exc)
#ValueError: value must be >0

a=LineItem('a_test',100,100)
b=LineItem('b_test',200,200)
print(a.__class__.weight) #<__main__.Quantity object at 0x00A80970>
print(b.__class__.weight) #<__main__.Quantity object at 0x00A80970> #<-같다! 디스크립터(Quantity)는 각 변수마다 한 개의 인스턴스만 있다는 것을 확인
print(a.__class__.price) #<__main__.Quantity object at 0x03BF0B30>
print(b.__class__.price) #<__main__.Quantity object at 0x03BF0B30>