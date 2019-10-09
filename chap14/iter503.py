#iter(object[, sentinel])
#https://docs.python.org/ko/3/library/functions.html?highlight=iter#iter
#이터레이터 객체를 돌려줍니다. 첫 번째 인자는 두 번째 인자의 존재 여부에 따라 매우 다르게 해석됩니다. 
#1. (__iter__ 혹은 __getitem__으로 다음 요소 순회)
#두 번째 인자가 없으면, object 는 이터레이션 프로토콜 (__iter__() 메서드)을 지원하는 컬렉션 객체이거나 시퀀스 프로토콜 (0에서 시작하는 정수 인자를 받는 __getitem__() 메서드)을 지원해야 합니다. 
#이러한 프로토콜 중 아무것도 지원하지 않으면 TypeError 가 일어납니다. 
#2. (sentinel값까지 함수(콜러블) 호출)
#두 번째 인자 sentinel 이 주어지면, object 는 콜러블이어야 합니다. 
#이 경우 만들어지는 이터레이터는 __next__() 메서드가 호출될 때마다 인자 없이 object 를 호출합니다
#반환된 값이 sentinel 과 같으면, StopIteration 을 일으키고, 그렇지 않으면 값을 돌려줍니다.

#아래는 1.에 대해 설명. 2.에 대한 설명은 iter_2_538.py

class Foo:
	def __iter__(self):
		pass

from collections import abc
assert issubclass(Foo, abc.Iterable) #<-따로 등록/상속하지 않아도 True
f=Foo()
assert isinstance(f, abc.Iterable) #<-따로 등록/상속하지 않아도 True

#단, 실제로 iterable하게 동작하는, __iter__는 없지만 __getitem__만 있는 클래스는 위의 타입 검사를 통과하지 못한다
from sentence501 import Sentence
print(issubclass(Sentence, abc.Iterable)) #False
g=Sentence('abc')
print(isinstance(g, abc.Iterable)) #False
print(iter(g)) #<iterator object at 0x000001F08901AD30> #<-iterable을 가져온다
#따라서, iterable한지 검사시에는, 그냥 iter(x)를 호출해보고 TypeError를 뱉는지 아닌지 보는 것임 (try-except 활용)

#반복형 객체(iterable (type) object) : iter()가 반복자를 가져올 수 있는 모든 객체 (__iter__(반복자를 리턴하는 구현 메서드)가 있는 객체 + __getitem__을 구현한 시퀀스 프로토콜 객체)
#반복자: iterator
s='ABC' #<-반복형
#for문 이용 반복
for char in s:
	print(char)
#while문 이용 반복
it=iter(s) #<-반복자 반환
while True:
	try:
		print(next(it)) #<-next는 반복자에서 다음 요소를 가져온다. 다 가져와서 다음 요소가 없다면 StopIteration 예외가 발생한다
	except StopIteration:
		del it
		break

#반복자 표준 인터페이스
#__next__() : 다음에 사용할 항목 반환. 항목이 더 이상 남아있지 않으면 StopIteration 예외 발생 (사용시엔 next(object) 로 호출)
#__iter__() : self 반환 (return self)

s3=Sentence('Pig and Pepper')
it=iter(s3)
print(repr(it)) #<iterator object at 0x0000024F40EA9F98>
print(next(it)) #Pig
print(next(it)) #and
print(next(it)) #Pepper
try:
	print(next(it)) #StopIteration (error)
except StopIteration:
	pass
print(list(it)) #[] #<-모두 소진되었고 비어있다
it=iter(s3) #<-다시 반복하려면 생성자를 새로 만들어야 한다. (반복자를 재설정하거나 채울 방법 없음)
print(list(it)) #['Pig', 'and', 'Pepper']