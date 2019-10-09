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
			discount=self.promotion(self) #<-
		return self.total()-discount
	def __repr__(self):
		fmt='<Order total: {:.2f} due: {:.2f}>'
		return fmt.format(self.total(),self.due())

def FidelityPromo(order): #strategy[0]
	"""충성도 1000 이상일 때 5% 할인"""
	return order.total()*0.05 if order.customer.fidelity>=1000 else 0

def BulkItemPromo(order): #strategy[1]
	"""20개 이상 동일상품 구매시 10% 할인"""
	discount=0
	for item in order.cart:
		if item.quantity>=20:
			discount+=item.total()*0.1
	return discount

def LargeOrderPromo(order): #strategy[2]
	"""10종류 이상 상품 구매시 7% 할인"""
	distinct_items={item.product for item in order.cart}
	if len(distinct_items)>=10:
		return order.total()*0.07
	return 0

##selecting best promotion
#1.
# promos=[FidelityPromo,BulkItemPromo,LargeOrderPromo]
# def best_promo(order):
# 	"""최대로 할인받을 수 있는 금액 반환"""
# 	return max(promo(order) for promo in promos)
#위 코드의 문제: 할인 전략을 추가/변경시 매우 짜증남.

#2.
promos=[globals()[name] for name in globals() if name.endswith('Promo') and name!='best_promo'] 
# globals(): 함수가 정의된 모듈의 전역 심볼 테이블을 dict로 반환
#따라서 이 코드는 globals(),즉 전역 심볼 테이블의 모든 values 중 Promo로 끝나는 것들을 리스트로 변환
#(구체전략 함수이름을 다 *Promo로 맞춰놓아 이것이 가능. (꼼수임...))
# print(promos) #for view
def best_promo(order):
	"""최대로 할인받을 수 있는 금액 반환"""
	return max(promo(order) for promo in promos)

#3. 구체전략 module을 분리 후, 로딩시 모든 함수를 모아서 이를 적용
# import promo_strategy_module #<-분리 모듈
# import inspect
# promos=[func for name, func in inspect.getmembers(promo_strategy_module,inspect.isfunction)] 
# #isfunction으로 검사해서 함수면 다 가져옴.. 필요시 인수 등을 더 검사하는 코드 추가할 수 있음. 혹은 전용 데커레이터 사용 등..
# def best_promo(order):
# 	return max(promo(order) for promo in promos)

#test
joe=Customer('John Doe',0)
ann=Customer('Ann Smith',1100)

cart=[LineItem('banana',4,0.5),LineItem('apple',10,1.5),LineItem('watermellon',5,5.0)]
print(Order(joe,cart,FidelityPromo))
print(Order(ann,cart,FidelityPromo))

banana_cart=[LineItem('banana',30,0.5),LineItem('apple',10,1.5)]
print(Order(joe,banana_cart,BulkItemPromo))

long_order=[LineItem(str(item_code),1,1.0) for item_code in range(10)]
print(Order(joe,long_order,LargeOrderPromo))
print(Order(joe,cart,LargeOrderPromo))

#new test for best_promo
print(Order(joe,long_order,best_promo))
print(Order(joe,banana_cart,best_promo))
print(Order(ann,cart,best_promo))