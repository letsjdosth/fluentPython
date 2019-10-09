from abc import ABC, abstractmethod
from collections import namedtuple

Customer=namedtuple('Customer','name fidelity')

class LineItem:
	def __init__(self,product,quantity,price):
		self.product=product
		self.quantity=quantity
		self.price=price
	def total(self):
		return self.price*self.quantity

class Order: #context
	def __init__(self,customer,cart,promotion=None):
		self.customer=customer
		self.cart=list(cart)
		self.promotion=promotion
	def total(self):
		if not hasattr(self,'__total'):
			self.__total=sum(item.total() for item in self.cart)
		return self.__total
	def due(self):
		if self.promotion is None:
			discount=0
		else:
			discount=self.promotion.discount(self)
		return self.total()-discount
	def __repr__(self):
		fmt='<Order total: {:.2f} due: {:.2f}>'
		return fmt.format(self.total(),self.due())

class Promotion(ABC): #strategy(abstract class)
	@abstractmethod
	def discount(self,order):
		"""할인액을 구체적인 숫자로 반환하는 것을 구현할 것"""

class FidelityPromo(Promotion): #strategy[0]
	"""충성도 1000 이상일 때 5% 할인"""
	def discount(self,order):
		return order.total()*0.05 if order.customer.fidelity>=1000 else 0

class BulkItemPromo(Promotion): #strategy[1]
	"""20개 이상 동일상품 구매시 10% 할인"""
	def discount(self,order):
		discount=0
		for item in order.cart:
			if item.quantity>=20:
				discount+=item.total()*0.1
		return discount

class LargeOrderPromo(Promotion): #strategy[2]
	"""10종류 이상 상품 구매시 7% 할인"""
	def discount(self,order):
		distinct_items={item.product for item in order.cart}
		if len(distinct_items)>=10:
			return order.total()*0.07
		return 0

joe=Customer('John Doe',0)
ann=Customer('Ann Smith',1100)

cart=[LineItem('banana',4,0.5),LineItem('apple',10,1.5),LineItem('watermellon',5,5.0)]
print(Order(joe,cart,FidelityPromo())) #참고: 원래의 전략 패턴은 context가 전략을 선택해야 함. 직접 선택해서 넣어주는 것이 아님
print(Order(ann,cart,FidelityPromo())) #여기서는 그냥 편의를 위해 이렇게 예시

banana_cart=[LineItem('banana',30,0.5),LineItem('apple',10,1.5)]
print(Order(joe,banana_cart,BulkItemPromo()))

long_order=[LineItem(str(item_code),1,1.0) for item_code in range(10)]
print(Order(joe,long_order,LargeOrderPromo()))
print(Order(joe,cart,LargeOrderPromo()))
 