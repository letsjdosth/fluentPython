#v6: 클래스 데코레이터 사용
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


#클래스 데코레이터로 쓸 함수. (클래스가 생성되는 순간 클래스의 클래스 선언을 수정한다!)
def entity(cls):
	# print('cls.__dict__:',cls.__dict__)  #<-아래 루프에 뭐가 넘어오는지 보고싶으면 이 문장을 주석 해제하고 bulkfood_v6을 실행
	for key, attr in cls.__dict__.items():
		if isinstance(attr, Validated):
			type_name=type(attr).__name__
			attr.storage_name='_{}#{}'.format(type_name, key) #1
	return cls #변경된 클래스 반환(이후 만드는 인스턴스는 storage_name이 위와같이 덮어써진채로 만들어진다)
	##1
	#cls.__dict__.attr(__dict__의 value).storage_name의 값을 직접 재설정한다.
	# if문이 참이 될 때 attr에 들어오는 요소
	# <model_v6.NonBlank object at 0x0144EC10>
	# <model_v6.Quantity object at 0x0145F8B0>
	# <model_v6.Quantity object at 0x01510B90>