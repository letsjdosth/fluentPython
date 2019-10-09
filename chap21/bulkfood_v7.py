##v7: metaclass 사용
import model_v7 as model

class LineItem(model.Entity): #<-model.Entity의 메타클래스 EntityMeta가 v6에서 데코레이터의 역할을 한다. 서브클래스에도 메타클래스가 확실히 적용되기 때문에, 간단히 Entity를 상속한다.
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