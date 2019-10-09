#목표: 실제 저장되는 저장소 이름을 구조의 이름대로 바꾸자.
#v6: 클래스 데코레이터 사용

import model_v6 as model

@model.entity #<-데코레이터 적용
class LineItem:
	description=model.NonBlank()
	weight=model.Quantity()
	price=model.Quantity()

	def __init__(self, description, weight, price):
		self.description=description
		self.weight=weight
		self.price=price
	def subtotal(self):
		return self.weight*self.price

if __name__=='__main__':
	raisins=LineItem('Golden raisins', 10, 6.95)
	print(dir(raisins)[:3]) #['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
	print(LineItem.description.storage_name) #_NonBlank#description
	print(raisins.description) #Golden raisins
	print(getattr(raisins, '_NonBlank#description')) #Golden raisins