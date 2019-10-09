#1. 객체와 클래스가 동일한 이름의 속성을 가지고 있으면, 객체 속성이 클래스 속성을 가린다
class TestClass:
	data='the class data attr'

	@property
	def prop(self):
		return 'the prop value'

obj=TestClass()
print(vars(obj)) #{} #<-!!없다 #참고: vars([object]) :모듈, 클래스, 인스턴스 또는 __dict__ 어트리뷰트가 있는 다른 객체의 __dict__ 어트리뷰트를 돌려줍니다.
print(obj.data) #the class data attr

obj.data='bar'
print(vars(obj)) #{'data': 'bar'}
print(obj.data) #bar

print(TestClass.data) #the class data attr
	

#2. 프로퍼티는 객체 속성에 의해 가려지지 않는다(클래스 정의가 우선된다)
print(TestClass.prop) #<property object at 0x01C62150> #<-클래스에서 직접 읽으면 프로퍼티 객체 자체가 나타난다
print(obj.prop) #the prop value #<-인스턴스에서 읽으면 게터를 실행하고 리턴값을 가져온다
try:
	obj.prop='foo' #AttributeError: can't set attribute #<-프로퍼티로 데코레이트해 만든 속성은 직접 할당할 수 없다
except AttributeError as exc:
	print('AttributeError: ',exc)

#직접 __dict__에 접근해 만들어보자
obj.__dict__['prop']='foo'
print(vars(obj)) #{'data': 'bar', 'prop': 'foo'}
print(obj.prop) #the prop value #<-객체 속성 prop을 가져오지 않고, 게터가 실행된다. 

#프로퍼티 객체를 지워보자
TestClass.prop='baz' #아무거나로 덮어써보면
print(obj.prop) #foo #<-이제 객체속성을 가져오게 된다


#3. 프로퍼티는 기존 객체 속성도 가린다.
#다시 만들어보자
print(obj.data) #bar
print(TestClass.data) #the class data attr
TestClass.data=property(lambda self: 'the "data" prop value') #프로퍼티 설정
print(obj.data) #the "data" prop value #<-다시 프로퍼티가 우선으로 올라와, 게터를 실행한다

#다시 또 지워보자
del TestClass.data #지우면
print(obj.data) #bar #다시 객체속성을 가져온다

#결론: obj.attr같은 표현식은 객체 obj에서부터 attr을 찾는것이 아님.
#일반적으로 변수검색 순서는 먼저 obj.__class__에서 찾고, 여기에 없을 경우에 다음으로 obj 객체의 속성(__dict__등)을 찾는다
