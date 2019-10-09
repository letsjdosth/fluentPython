#기존 방식
class Dog1:
	def __init__(self, name, weight, owner):
		self.name=name
		self.weight=weight
		self.owner=owner #<-같은방식으로 3번을 써야한다.짜증
rex1=Dog1('Rex',30,'Bob')
print(rex1) #<__main__.Dog object at 0x037BF690> #<-출력이, 안에 뭐가 들어있는지 바로 안 보인다


#클래스 팩토리 도입
def record_factory(cls_name, field_names):
	try:
		field_names=field_names.replace(',',' ').split()
	except AttributeError: #replace, split을 못 쓸 때
		pass #그냥 시퀀스로 되어있다고 가정한다
	field_names=tuple(field_names)

	def __init__(self,*args,**kwargs):
		attrs=dict(zip(self.__slots__, args))
		attrs.update(kwargs)
		for name, value in attrs.items():
			setattr(self, name, value)

	def __iter__(self):
		for name in self.__slots__:
			yield getattr(self, name)

	def __repr__(self):
		values=', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
		return '{}({})'.format(self.__class__.__name__, values)

	cls_attrs=dict(__slots__=field_names, __init__=__init__, __iter__=__iter__, __repr__=__repr__) #클래스 속성 조합
	return type(cls_name, (object,), cls_attrs) #클래스 생성 후 반환. type은 아래에 설명. 
	#(단, 이렇게 만들면 직렬화할수 없다)


Dog2=record_factory('Dog','name weight owner')
rex2=Dog2('Rex',30,'Bob')
print(rex2) #Dog(name='Rex', weight=30, owner='Bob')
name, weight, _=rex2
print(name, weight) #Rex 30
print("{2}'s dog weighs {1}kg".format(*rex2)) #Bob's dog weighs 30kg
rex2.weight=32
print(rex2) #Dog(name='Rex', weight=32, owner='Bob')
print(Dog2.__mro__) #(<class '__main__.Dog'>, <class 'object'>) #<-팩토리와는 아무런 상관이 없다.


#참고: type
class MySuperClass:
	pass
class MyMixin:
	pass
MyClass=type('MyClass',(MySuperClass, MyMixin), {'x':42, 'x2':lambda self:self.x*2})
#인자3개: 클래스 이름, 베이스클래스(상속해올 부모클래스), 속성dict
#반환값은 '클래스'이다. (인스턴스가 아님!)
#위 코드는 아래와 같이 작동한다
class MyClass(MySuperClass,MyMixin):
	x=42
	def x2(self):
		return self.x*2
