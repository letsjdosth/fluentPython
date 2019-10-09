#v1과 동일하지만, 데커레이터를 사용하지 않는 고전적인 방식의 프로퍼티
class LineItem:
	def __init__(self, description, weight, price):
		self.description=description
		self.weight=weight
		self.price=price

	def subtotal(self):
		return self.weight*self.price

	def get_weight(self):
		return self.__weight

	def set_weight(self, value):
		if value>0:
			self.__weight=value
		else:
			raise ValueError('value must be >0')

	weight=property(get_weight,set_weight)
#class property(fget=None, fset=None, fdel=None, doc=None)
# https://docs.python.org/ko/3/library/functions.html?highlight=property#property
# 프로퍼티 어트리뷰트를 돌려줍니다.
# fget 은 어트리뷰트 값을 얻는 함수입니다(게터). fset 은 어트리뷰트 값을 설정하는 함수입니다(세터). fdel 은 어트리뷰트 값을 삭제하는 함수입니다(딜리터). 그리고 doc 은 어트리뷰트의 독스트링을 만듭니다.
# (C가 클래스이고 x라는 프로퍼티가 정의되어 있을 때, 차례대로 C.x, C.x=value, del C.x가 호출될 때 해당 함수로 넘겨줌)
# (마찬가지의 상황에서, 대응되는 데코레이터는 @property, @x.setter, @x.deleter) 