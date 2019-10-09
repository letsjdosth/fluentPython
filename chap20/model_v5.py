#목표: 디스크립터 확장을 위한 속성관리-검증 분리
#이 디스크립터 구조는 bulkfood_v5에서 사용한다.

#(관리)         (검증)     (검증조건구상클래스)
#AutoStorage <- Validated <-Quantity
#                         <-Nonblank

#참고: 각 디스크립터 클래스의 독스트링은 관리대상객체의 help에서 각 속성에 대한 도움말로 보이게 된다.
#예. 파이썬쉘에서 bulkfood_v5.py 임포트 후
# >>> help(LineItem)
# Help on class LineItem in module __main__:

# class LineItem(builtins.object)
#  |  LineItem(description, weight, price)
#  |  
#  |  Methods defined here:
#  |  
#  |  __init__(self, description, weight, price)
#  |      Initialize self.  See help(type(self)) for accurate signature.
#  |  
#  |  subtotal(self)
#  |  
#  |  ----------------------------------------------------------------------
#  |  Data descriptors defined here:
#  |  
#  |  __dict__
#  |      dictionary for instance variables (if defined)
#  |  
#  |  __weakref__
#  |      list of weak references to the object (if defined)
#  |  
#  |  description
#  |      최소 하나 이상의 비공백 문자가 들어있는 문자열
#  |  
#  |  price
#  |      0보다 큰 수
#  |  
#  |  weight
#  |      0보다 큰 수

import abc

class AutoStorage:
	'''저장소 속성 관리만 한다. (검증은 자식 클래스에 위임)'''
	__counter=0

	def __init__(self):
		cls=self.__class__
		prefix=cls.__name__
		index=cls.__counter
		self.storage_name='_{}#{}'.format(prefix, index)
		cls.__counter+=1

	def __set__(self,instance,value):
			setattr(instance, self.storage_name, value) #더이상 조건으로 거르지 않는다

	def __get__(self,instance,owner):
		if instance is None:
			return self
		else:
			return getattr(instance, self.storage_name)


class Validated(abc.ABC, AutoStorage):
	def __set__(self, instance, value):
		value=self.validate(instance, value) #<-여기서 거른다. 리턴값을 집어넣기 때문에 유효한 데이터만 리턴되도록 만든다.
		super().__set__(instance,value)

	@abc.abstractmethod #추상클래스화해 자식클래스가 구상할 것을 강제한다
	def validate(self, instance, value):
		'''검증된 값을 반환하거나, ValueError 를 발생시킨다'''



#조건들은 Validated를 상속받아 validate()를 오버라이드해 명시
class Quantity(Validated):
	'''0보다 큰 수'''
	def validate(self, instance, value):
		if value <=0:
			raise ValueError('value must be >0')
		else:
			return value


class NonBlank(Validated):
	'''최소 하나 이상의 비공백 문자가 들어있는 문자열'''
	def validate(self, instance, value):
		#이 사이에서 데이터를 정리/변환/정규화해볼 수 있다
		value=value.strip()
		if len(value)==0:
			raise ValueError('value cannot be empty or blank')
		else:
			return value