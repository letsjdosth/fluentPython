#클래스 안에서 속성 하나하나마다 @prperty, @x.setter를 달아주기 귀찮다
#팩토리를 만들어서 간단하게 하자

def quantity(storage_name):
	'''property factory'''
	def qty_getter(instance): #<-class 안에서 instance는 self가 들어가게 된다
		return instance.__dict__[storage_name] #<-instance.storage_name에서 가져오게 하면 논리상 무한호출된다. __dict__에서 직접 가져오자.
	def qty_setter(instance, value):
		if value>0:
			instance.__dict__[storage_name]=value #<-마찬가지로 __dict__에 직접 설정하자
		else:
			return ValueError('value must be >0')
	return property(qty_getter,qty_setter)

class LineItem:
	weight=quantity('weight')
	price=quantity('price')

	def __init__(self, description, weight, price):
		self.description=description
		self.weight=weight
		self.price=price

	def subtotal(self):
		return self.weight*self.price

#for test
if __name__=='__main__':
	nutmeg=LineItem('Moluccan nutmeg',8,13.95)
	print(nutmeg.weight, nutmeg.price) #8 13.95
	print(sorted(vars(nutmeg).items())) #[('description', 'Moluccan nutmeg'), ('price', 13.95), ('weight', 8)]