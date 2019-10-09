#v4 목표: weight=Quentity('weight')<-weight를 2번 써야되서 맘에 안든다. 개선하자
#v4b 목표: 내부조사/메타프로그래밍을 위해 Quantity의 인스턴스에 접근할 수 있도록 하자

class Quantity:
	__counter=0

	def __init__(self):
		cls=self.__class__
		prefix=cls.__name__
		index=cls.__counter
		self.storage_name='_{}#{}'.format(prefix, index)
		cls.__counter+=1

	def __set__(self,instance,value):
		if value>0:
			setattr(instance, self.storage_name, value)
			
		else:
			raise ValueError('value must be >0')
	def __get__(self,instance,owner):#<-인스턴스가 아닌 클래스 LineItem을 통해 관리대상 속성을 가져올 때는 instance로 None을 받는다.(v4버전의 test 참조)
		if instance is None:
			return self #<-self를 돌려줘서, Quantity 인스턴스에 접근할 수 있게 하자
		else:
			return getattr(instance, self.storage_name)


class LineItem:
	weight=Quantity()
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
	print('AttributeError',exc) #기존 v4는 이 에러가 났다. #AttributeError 'NoneType' object has no attribute '_Quantity#0' '_Quantity#0'
else:
	print('↑ access to Quantity instance!')
# <__main__.Quantity object at 0x0112F690>
# ↑ access to Quantity instance!