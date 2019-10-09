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

#4. using decorator for collecting promotion func
promos=[]
def promotion(promo_func):
	promos.append(promo_func)
	return promo_func

@promotion  #<-promo decorator 추가
def FidelityPromo(order): #strategy[0]
	"""충성도 1000 이상일 때 5% 할인"""
	return order.total()*0.05 if order.customer.fidelity>=1000 else 0

@promotion
def BulkItemPromo(order): #strategy[1]
	"""20개 이상 동일상품 구매시 10% 할인"""
	discount=0
	for item in order.cart:
		if item.quantity>=20:
			discount+=item.total()*0.1
	return discount

@promotion
def LargeOrderPromo(order): #strategy[2]
	"""10종류 이상 상품 구매시 7% 할인"""
	distinct_items={item.product for item in order.cart}
	if len(distinct_items)>=10:
		return order.total()*0.07
	return 0

def best_promo(order):
	"""최대로 할인받을 수 있는 금액 반환"""
	return max(promo(order) for promo in promos) 

#이제 구체적인 strategy function이 특별한 이름형태로 되어있을 필요가 없음
#코드 가독성도 좋음
#프로모션 추가/배제가 편함. 추가시 데커레이터만 달아주면 됨. 배제시 데커레이터만 빼주면 됨. 
#또한 데커레이터만 import하면 어느 모듈에서도 프로모션 정의 가능. 굳이 특정 모듈에서 있을 이유가 없음 (물론 정리상의 이점은 있지만..)


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