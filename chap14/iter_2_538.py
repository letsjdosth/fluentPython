#iter(object[, sentinel])
#https://docs.python.org/ko/3/library/functions.html?highlight=iter#iter
#이터레이터 객체(반복자)를 돌려줍니다. 첫 번째 인자는 두 번째 인자의 존재 여부에 따라 매우 다르게 해석됩니다. 
#1. (__iter__ 혹은 __getitem__으로 다음 요소 순회)
#두 번째 인자가 없으면, object 는 이터레이션 프로토콜 (__iter__() 메서드)을 지원하는 컬렉션 객체이거나 시퀀스 프로토콜 (0에서 시작하는 정수 인자를 받는 __getitem__() 메서드)을 지원해야 합니다. 
#이러한 프로토콜 중 아무것도 지원하지 않으면 TypeError 가 일어납니다. 
#2. (sentinel값까지 함수(콜러블) 호출)
#두 번째 인자 sentinel 이 주어지면, object 는 콜러블이어야 합니다. 
#이 경우 만들어지는 이터레이터는 __next__() 메서드가 호출될 때마다 인자 없이 object 를 호출합니다
#반환된 값이 sentinel 과 같으면, StopIteration 을 일으키고, 그렇지 않으면 값을 돌려줍니다.

#아래는 2.에 대해 설명. 1.에 대한 설명은 iter_503.py

from random import randint
def d6():
	return randint(1,6)

d6_iter=iter(d6,1) #<-d6을 한번씩 실행해 값을 생성해 반환하며, 1이나오면 StopIteration 예외를 내고 중지하는 이터레이터를 생성한다
print(d6_iter) #<callable_iterator object at 0x000001DF512CD0B8>


while True:
	try:
		print(next(d6_iter))
	except StopIteration:
		print('StopIteration')
		break

d6_iter=iter(d6,1) #재생성. 기존것은 StopIteration 이후 비게 된다
for roll in d6_iter:
	print(roll)
	#for문은 StopIteration이 나오면 자체적으로 예외를 잡고 중지하므로, 따로 예외처리를 하지 않아도 된다


#공식문서 예시
def process_each_one_line(filename,process_line:callable):
	with open(filename) as fp:
		for line in iter(fp.readline,''):
			process_line(line)