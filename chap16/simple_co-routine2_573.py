def simple_coro2(a):
	print('-> Started: a=',a)
	b=yield a
	print('-> Received: b=',b)
	c=yield a+b
	print('-> Received: c=',c)

my_coro2=simple_coro2(14)

from inspect import getgeneratorstate
print(getgeneratorstate(my_coro2)) #GEN_CREATED #<-실행 시작 대기
next(my_coro2) #기동(priming)(처음 나오는 yield까지 진행시키기)
# -> Started: a= 14
# 14 #<-서브라임텍스트 결과창에서는 안보인다. print문 사용 혹은 인터프리터에서 볼 것
#내부적으로는 'yield문이 있는 행의 대입연산자 직전(즉 오른쪽 표현식)까지 진행'한다. 즉 yield a 까지 진행하여 숫자 14를 생성한 다음 대기한다.
#코드 읽을 때 주의할것! a를 생성해서 b에 넣는것이 아니다. a를 생성해 외부 코드로 주고 멈춘 후, 다음 이 제너레이터의 next가 호출되면 새 값을 받아 b에 넣는다.

print(getgeneratorstate(my_coro2)) #GEN_SUSPENDED #<-yield문 대기
my_coro2.send(28)
# -> Received: b= 28
# 42
#내부적으로는, send()로 받은 28을 b에 대입하는 것으로 시작하고, 중간 코드를 실행한 후, a+b를 계산하여 yield a+b를 생성한 후 대기한다. c에 대입할 값을 기다린다.

try:
	my_coro2.send(99)
except StopIteration:
	print('StopIteration')
	pass
# -> Received: c= 99
# StopIteration
#내부적으로는, send()로 받은 99를 c에 대입하고 중간 코드를 실행한다. 제너레이터 함수의 끝에 도달했으므로 StopIteration 예외를 발생시키고 끝난다.

print(getgeneratorstate(my_coro2)) #GEN_CLOSED #<-실행 완료