#v7: metaclass 사용

import abc

class AutoStorage:
	'''저장소 속성 관리만 한다.(검증은 자식 클래스에 위임)'''
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


#메타클래스 (v6의 데코레이터 역할)
class EntityMeta(type):
	"""검증된 필드를 가진 비즈니스 개체에 대한 메타클래스"""
	def __init__(cls, name, bases, attr_dict):
		# print('name:',name,'bases:',bases,'attr_dict:',attr_dict) #<-뭐가 넘어오는지 보고싶으면 이 문장을 주석 해제하고 bulkfood_v7을 실행
		super().__init__(name,bases,attr_dict)
		for key, attr in attr_dict.items():
			if isinstance(attr, Validated):
				type_name=type(attr).__name__
				attr.storage_name='_{}#{}'.format(type_name, key)

class Entity(metaclass=EntityMeta):
	"""검증된 필드를 가진 비즈니스 객체 """
	#사용자가 메타클래스를 신경쓰지 않고 단지 Entity 클래스를 상속하면 되도록 함. 오직 편의를 위한 정의임.