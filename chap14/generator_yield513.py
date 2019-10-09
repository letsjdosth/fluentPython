#제너레이터 함수: yield를 가진 함수. 호출되면 제너레이터 객체 반환
#리턴되는 제너레이터(generator)는 yield 에 전달된 표현식의 값을 차례대로 '생성'하는 반복자(iterator)
#기존 상태에서 계산을 중단했다가 next() 호출 시 이어서 다음 yield까지 진행 후 값 생성. 다음 호출을 위해 제너레이터는 이 상태를 기억한다
#함수의 끝에 도달하거나 return을 만나면 StopIteration을 돌려줌(iterator protocol에 맞춰줌)
#(제너레이터 함수는 일종의 제너레이터 팩토리임)
#생성할 값을 처음부터 모두 만들어 둘 필요가 없다. 필요한 값만 yield 명령 직전에/동시에 생성하면 된다. 제너레이터는 느긋하게 구현하기 위한 설계임

#example 1
def gen_123():
	yield 1
	yield 2
	yield 3

#for test
print(gen_123) #<function gen_123 at 0x000001C012721E18> #<-그냥 함수취급이다
print(gen_123()) #<generator object gen_123 at 0x000002D11743A780> #<-제너레이터 객체를 반환한다

for i in gen_123(): 
	print(i)
#1
#2
#3

g=gen_123()
next(g) #1 #<-next()가 작동한다. generator object는 반복자
next(g) #2
next(g) #3
try:
	next(g) #StopIteration #<-반복자 프로토콜을 잘 지킴.
except StopIteration:
	pass
#참고:for문
# for a in b:
# c=iter(b)를 만들고 next(c)를 호출 후 그 반환값을 a에 할당한다
# 이후 for문 블럭 실행.
# 다시 next(c)를 호출 후 그 반환값을 a에 할당한다.
# 이를 반복
# a가 StopIteration이면, 멈춘다


#example 2
def gen_AB():
	print('start')
	yield 'A'
	print('continue')
	yield 'B'
	print('end.')

for c in gen_AB():
	print('-->',c)
# start
# --> A
# continue
# --> B
# end.


