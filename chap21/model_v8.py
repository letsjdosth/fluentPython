#__prepare__를 이용해, 메타클래스에 attr를 넘기는 부분에 ordereddict 사용

import abc
import collections

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
	"""검증된 필드를 가진 비즈니스 객체에 대한 메타클래스. 관리대상 객체에서 선언한 속성의 순서를 보존하며 처리한다."""
	
	@classmethod #언제나 __prepare__는 classmethod여야 한다.
	def __prepare__(cls,name,bases):
		return collections.OrderedDict() #<-빈 OrderedDict

	def __init__(cls, name, bases, attr_dict):
		# print('name:',name,'bases:',bases,'attr_dict:',attr_dict) #<-뭐가 넘어오는지 보고싶으면 이 문장을 주석 해제하고 bulkfood_v8을 실행
		super().__init__(name,bases,attr_dict)
		cls._field_names=[] #<-v8
		for key, attr in attr_dict.items():
			if isinstance(attr, Validated):
				type_name=type(attr).__name__
				attr.storage_name='_{}#{}'.format(type_name, key)
				cls._field_names.append(key) #<-v8. Validated인 필드를 해당 리스트에 추가함

#참고: 해당 프린트문을 실행하면
#name: LineItem bases: (<class 'model_v8.Entity'>,) 
#attr_dict: OrderedDict([('__module__', '__main__'), ('__qualname__', 'LineItem'), ('description', <model_v8.NonBlank object at 0x014FF8B0>), ('weight', <model_v8.Quantity object at 0x032C0B50>), ('price', <model_v8.Quantity object at 0x03377B10>), ('__init__', <function LineItem.__init__ at 0x032C8540>), ('subtotal', <function LineItem.subtotal at 0x033AD228>)])
#attr_dict가 OrderedDict인 것을 확인할 수 있다. __prepare__에서 빈것을 넘기면, 실제로 메타클레스 동작시 __init__에 들어오는 attr_dict 자리에 내용이 채워져 들어온다.


class Entity(metaclass=EntityMeta):
	"""검증된 필드를 가진 비즈니스 객체 """
	@classmethod
	def field_names(cls):
		"""EntityMeta의 __init__의 for문에서 추가된 순서대로 속성 이름을 반환하는 제너레이터"""
		for name in cls._field_names:
			yield name
