import model_v5 as model

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

#for test
if __name__=='__main__':
	try:
		truffle=LineItem('White truffle',100,0)
	except ValueError as exc:
		print('ValueError:',exc)
	#ValueError: value must be >0

	try:
		blk=LineItem('',100,200)
	except ValueError as exc:
		print('ValueError:',exc)

	valid_item=LineItem('Valid!',100,200)
	print(valid_item.weight, valid_item.price, valid_item.subtotal()) #100 200 20000

	print(valid_item.__dict__) #{'_NonBlank#0': 'Valid!', '_Quantity#0': 100, '_Quantity#1': 200} #<- self.__class__.__name__이 첫 {}에 들어가므로 이렇게 된다.
	print(getattr(valid_item,'_Quantity#0'),getattr(valid_item,'_Quantity#1'),getattr(valid_item,'_NonBlank#0')) #100 200 Valid!

	try:
		print(valid_item.__class__.weight)
	except AttributeError as exc:
		print('AttributeError',exc)
	else:
		print('↑ access to Quantity instance!')
	# <model_v5.Quantity object at 0x02D40970>
	# ↑ access to Quantity instance!
