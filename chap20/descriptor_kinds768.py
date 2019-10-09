
#보조함수
def cls_name(obj_or_cls):
	'''해당 클래스의 이름(__name__의 맨 마지막 . 뒤)을 반환한다'''
	cls=type(obj_or_cls)
	if cls is type: 
		cls=obj_or_cls
		#참고: type은 type들 자체의 클래스임. type(3)==int, type(int)==type, print(type)==<class 'type'>. type의 type은 type임.
		#위 조건문에선 is를 쓰므로, 포인터가 같아야(가리키는 메모리주소가 같아야)함. 따라서 cls가 type 자체일 때만 True, 아닐때는(int/string 등일때도) False
	return cls.__name__.split('.')[-1]

def display(obj):
	'''obj의 type관련 스트링을 만든다'''
	cls=type(obj)
	if cls is type:
		return '<class {}>'.format(obj.__name__)
	elif cls in [type(None), int]:
		return repr(obj)
	else:
		return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
	pseudo_args=', '.join(display(x) for x in args)
	print('-> {}.__{}__({})'.format(cls_name(args[0]),name,pseudo_args))


#범주별 디스크립터 선언
class Overriding:
	"""__set__을 구현하면 오버라이딩 디스크럽터라고 부른다. 데이터 디스크립터 혹은 강제 디스크립터라고도 부른다"""
	def __get__(self, instance, owner):
		print_args('get', self, instance, owner)

	def __set__(self, instance, value):
		print_args('set', self, instance, value)

class OverridingNoGet:
	"""__get__이 없는 오버라이딩 디스크립터"""
	def __set__(self, instance, value):
		print_args('set', self, instance, value)

class NonOverriding:
	"""__set__이 없으므로 논오버라이딩 디스크립터이다. 비데이터 디스크립터 혹은 가릴 수 있는 디스크립터라고도 부른다"""
	def __get__(self, instance, owner):
		print_args('get', self, instance, owner)

#관리대상 클래스
class Managed:
	over=Overriding()
	over_no_get=OverridingNoGet()
	non_over=NonOverriding()

	def spam(self):
		"""메서드도 일종의 디스크립터이다"""
		print('-> Managed.spam({})'.format(display(self)))


#for test
obj=Managed()

#1. 오버라이딩 디스크립터(__set__ 구현됨) 테스트
obj.over #-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>) #<-__get__이 동작했다. 참고로 owner 자리에는 부른 클래스에 대한 참조가 들어간다.
Managed.over #-> Overriding.__get__(<Overriding object>, None, <class Managed>) #<-클래스를 통해 접근하면 instance 자리에 None이 넘겨진다

obj.over=7 #-> Overriding.__set__(<Overriding object>, <Managed object>, 7) #<-__set__이 동작했다. (구현상 실제로 7이 써지진 않는다)
obj.over #-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>) #<-기존대로 동작한다.

obj.__dict__['over']=8 #<-직접 over에 8을 써보자 
print(vars(obj)) #{'over': 8}
obj.over #-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>) #<-8이 안 나오고 __get__이 동작한다. 객체에 같은 이름 속성이 있어도 여전히 디스크립터에 의해 가로채진다.


#2. get이 없는 오버라이딩 디스크립터 테스트
print(obj.over_no_get) #<__main__.OverridingNoGet object at 0x010F0BB0> #<-__get__이 없으므로 그냥 디스크립터 객체를 반환한다.
print(Managed.over_no_get) #<__main__.OverridingNoGet object at 0x010F0BB0> #<-마찬가지이다.
obj.over_no_get=7 #-> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7) #<-__set__ 동작. 구현상 실제로 7이 쓰여지지는 않는다.
print(obj.over_no_get) #<__main__.OverridingNoGet object at 0x010F0BB0> #<-쓰여지지 않았으므로, 기존처럼 객체 자체를 반환한다.
obj.__dict__['over_no_get']=9 #<-직접 over_no_get에 9를 할당해보자
print(vars(obj)) #{'over': 8, 'over_no_get': 9}
print(obj.over_no_get) #9 #<-디스크립터에 __get__이 없으므로 파이썬 기본동작대로 그냥 obj 객체의 속성값을 반환한다. 이제 객체 속성이 디스크립터를 가린다.
obj.over_no_get=7  #-> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7) #여전히 할당시에는 __set__으로 가로채져 동작한다.
print(obj.over_no_get) #9


#3. 논오버라이딩 디스크립터(__set__ 구현되지 않음) 테스트
obj.non_over #-> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>) #<-디스크립터의 __get__이 동작했다.
obj.non_over=7 #<-__set__이 없으므로, 할당시 파이썬 기본동작을 한다. (!!!)
print(obj.non_over) #7 #!!!<-동일이름 객체 속성에 값이 들어가면, __get__이 호출되어야 할 것 같은 상황에도 호출되지 않고 디스크립터가 가려진다!
Managed.non_over #-> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>) #<-클래스로 접근 시 여전히 디스크립터가 읽기연산을 가로챈다
del obj.non_over #객체속성을 제거해보자
obj.non_over #-> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>) #<-다시 디스크립터의 __get__이 동작한다.

#중간 결론: 디스크립터는 __set__이 정의되어있냐에 따라 다르게 동작한다
#__set__이 정의되면, 정의된 디스크립터는 __get__이든 __set__이든 언제나 동작한다.(강제<라고 부르는 이유!)
#__set__이 정의되지 않으면, 디스크립터는 인스턴스에 같은이름 속성에 값이 할당되어버릴 때 가려진다.


#4. 클래스 자체에서 디스크립터를 덮어써버리는 경우
Managed.over=1
Managed.over_no_get=2
Managed.non_over=3
print(obj.over, obj.over_no_get, obj.non_over) #8 9 3 #<-몽땅 덮어써지고 디스크립터는 사라진다.
#클래스 속성에 저장하는 연산을 통제하려면 클래스의 클래스(메타클래스)에 디스크립터를 연결해야 함
#기본적으로 사용자정의 클래스의 메타클래스는 type이지만, 여기엔 속성을 추가할 수 없으므로, 사용자 정의 메타클래스를 구현해야 함


#5 메서드==논오버라이딩 디스크립터 (참고: 모든 사용자정의 함수는 __get__을 가지고 있다)
print(obj.spam) #<bound method Managed.spam of <__main__.Managed object at 0x039C0C10>> #<-객체를 통해 접근하면 __get__은 바인딩된 메서드 객체(첫 인수로 인스턴스를 넣는)를 반환한다. 
print(Managed.spam) #<function Managed.spam at 0x039C9618> #<-그냥 함수가 튀어나왔다. 관리대상 클래스를 통해 접근할 때는 __get__이 자기자신을 반환한다.
obj.spam=7 #<-인스턴스에, 메서드와 같은 이름의 값을 할당해보자
print(obj.spam) #7 #<-클래스속성인 함수가 가려진다. 즉, 메서드는 논오버라이딩 디스크립터처럼 동작한다. (참고: 함수는 __set__이 없다)
