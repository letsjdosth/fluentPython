#목표: weight=Quentity('weight')<-weight를 2번 써야되서 맘에 안든다. 개선하자

class Quantity:
	__counter=0 #<-self가 없다. 클래스속성.

	def __init__(self):
		cls=self.__class__
		prefix=cls.__name__ #Quantity
		index=cls.__counter
		self.storage_name='_{}#{}'.format(prefix, index) ##을 쓰면, 사용자가 지정한 속성명이랑 절대 충돌하지 않게 된다 (#은 주석처리 기호이고 \#은 속성명으로 허용이 안 됨..)
		cls.__counter+=1

	def __set__(self,instance,value):
		if value>0:
			setattr(instance, self.storage_name, value) #<-storage_name에 저장한다. 즉,_Quantity#0 와 같이 생긴  이름에 대신 저장한다.
			#<-실제 저장되는 이름과 저장을 요청하는 변수의 이름이 다르므로 이번엔 instance.__dict__에서 직접 읽지 않고 대신 setattr을 시용해도 무한재귀호출에 빠지지 않는다.
		else:
			raise ValueError('value must be >0')
	def __get__(self,instance,owner): #<-owner는 관리 대상 클래스(LineItem)에 대한 참조. #<-클래스를 통해(즉,LineItem을 통해) 관리대상 속성을 가져올 때는 instance로 None을 받는다.(밑 test 참조)
		return getattr(instance, self.storage_name) #마찬가지로 __dict__에서 직접 읽는 대신 getattr을 사용해도 괜찮다


class LineItem:
	weight=Quantity() #<-클래스 공개속성. 이젠 인수로 자기 이름을 안 넘겨도 된다.
	price=Quantity()
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

a=LineItem('a_test',100,200)
print(a.weight, a.price, a.subtotal()) #100 200 20000

print(a.__dict__) #{'description': 'a_test', '_Quantity#0': 100, '_Quantity#1': 200}
print(getattr(a,'_Quantity#0'),getattr(a,'_Quantity#1')) #100 200

try:
	print(a.__class__.weight)
except AttributeError as exc:
	print('AttributeError',exc) #AttributeError 'NoneType' object has no attribute '_Quantity#0' #<-__get__이 받는 instance가 None이 되기 때문에 이런 에러가 뜬다.
	#내부구현에 관련된 에러기때문에 에러메시지를 바꿔주는 것이 좋다.
