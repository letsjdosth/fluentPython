#v4에서 영감을 얻은 개선. 프로퍼티 팩토리 함수로 구현할 때도 이름을 받지 말자

def quantity(): #인수를 안 받는다
	'''property factory'''
	try:
		quantity.counter+=1
	except AttributeError:
		quantity.counter=0 #<-파이썬 함수 자체도 속성을 가질 수 있으므로, 이를 이용하자
	storage_name='_{}:{}'.format('quantity',quantity.counter)

	def qty_getter(instance): #<-class 안에서 instance는 self가 들어가게 된다
		return getattr(instance,storage_name)
	def qty_setter(instance, value):
		if value>0:
			setattr(instance, storage_name, value)
		else:
			return ValueError('value must be >0')
	return property(qty_getter,qty_setter)

class LineItem:
	weight=quantity() #<-변화
	price=quantity()

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
	print(sorted(vars(nutmeg).items())) #[('_quantity:0', 8), ('_quantity:1', 13.95), ('description', 'Moluccan nutmeg')]