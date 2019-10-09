'''
Introspection(or replection)
객체의 메타데이터(객체의 클래스, 구현 메소드, 프로퍼티, 프로토콜 등의 객체 정보)를 조사하는 과정
'''
def factorial(n):
	'''returns n!'''
	return 1 if n<2 else n*factorial(n-1)
#dir(): 어떤 객체를 인자로 넣어주면 해당 객체가 어떤 변수와 메소드(method)를 가지고 있는지 나열해줍니다.
print(dir(factorial))
#['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__',
# '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__',
# '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__',
# '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']

#__dict__
factorial.Annotaion ='test Annotaion' #!!:함수에도 class attribute 쓰듯 속성을 지정할 수 있다. (파이썬에서 둘은 같은 식으로 구현되어있기 때문)
print(factorial.__dict__) #{'Annotaion': 'test Annotaion'}  #__dict__에 저장된다.


#func 고유 속성
class C: pass
obj=C()
def func(): pass
print(sorted(set(dir(func))-set(dir(obj))))
#['__annotations__',       '__call__', '__closure__', '__code__',                         ,'__defaults__',  
# 매개변수/반환값 dict 주석, ()연산 구현, 함수 클로저,   바이트코드 컴파일 함수 메타데이터+본체  , 형식 매개변수 기본값,
#'__get__',                      '__globals__',       '__kwdefaults__',             '__name__', '__qualname__']
#읽기전용 디스크립터 프로토콜 구현, 함수정의모듈의 전역변수, 키워드전용형식매개변수 기본값, 함수이름,   pep3155 관련

