#코루틴 예외처리
#generator.throw(exc_type[, exc_value[, traceback]])
#제너레이터가 중단된 곳의 yield 표현식에 예외를 전달한다.
#제너레이터가 내부적으로 예외를 처리하면, 다음 yield문까지 진행되고, 생성된 값이 generator.throw의 호출값이 된다.(즉, 다음 yield문의 = 오른쪽까지 돌고 값을 제대로 생성한다)
#제너레이터가 내부적으로 예외를 처리하지 않으면, 다시 호출자로 해당 예최가 전파된다

class DemoException(Exception):
	"""실험용 예외 유형"""

def demo_exc_handling():
	print('-> coroutine started')
	while True:
		try:
			x=yield
		except DemoException:
			print('*** DemoException handled. Continueing...')
		else:
			print('->coroutine received: {!r}'.format(x))
	raise RuntimeError('This line should never run.') 
	#실제로는, 어떤일이 일어나도 19 라인은 실행되지 않는다. 
	#예외가 안 나거나 제대로 처리되면 계속해서 while문이 돌며
	#예외가 나면 곧바로 제너레이터가 정지된다
	#코루틴이 어떻게 끝나든 정리코드를 실행해야 하는 경우에는 try-finally구문 이용 (demo_2 참고)

#for test
from inspect import getgeneratorstate
exc_coro=demo_exc_handling()
next(exc_coro)
print(exc_coro.send(11))
print(exc_coro.send(22))
#처리된 예외 던지기
exc_coro.throw(DemoException) #*** DemoException handled. Continueing...
print(getgeneratorstate(exc_coro)) #GEN_SUSPENDED #<-정지되지 않았다
print(exc_coro.send(33)) #<-잘 돈다
#처리되지 않은 예외 던지기
exc_coro.throw(ZeroDivisionError) #ZeroDivisionError #<-호출 위치인 이 곳으로 ZeroDivisionError가 전파되어 돌아온다.
print(getgeneratorstate(exc_coro)) ##GEN_CLOSED  #<-인터프리터에서 실행