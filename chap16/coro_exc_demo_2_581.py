#코루틴 예외처리(계속)
#generator.close()
#제너레이터가 실행을 중단하고 기다리고 있는 yield 위치에 GeneratorExit 예외를 발생시킨다.
#제너레이터가 이 GenerationExit 예외를 처리하지 않거나 StopIteration 예외를 발생시키면, 호출자에는 이 에러들을 전파하지 않고 제너레이터를 중단시킨다.
#(주의! 닫다가 생기는 다른 예외는 호출자에게 전파한다!)
#단, GeneratorExit 예외를 처리한 결과의 다음 yield문은 아무런 값도 생성하지 않아야 하며, 아니면 RuntimeError가 발생하고 이는 호출자에 전달된다.



class DemoException(Exception):
	"""실험용 예외 유형"""

def demo_exc_handling():
	print('-> coroutine started')
	try: #코루틴이 어떻게 끝나든 정리코드를 실행해야 하는 경우에는 try-finally구문 이용
		while True:
			try:
				x=yield
			except DemoException:
				print('*** DemoException handled. Continueing...')
			else:
				print('->coroutine received: {!r}'.format(x))
	finally:
		print('->coroutine ending')


#for test
from inspect import getgeneratorstate
exc_coro=demo_exc_handling()
next(exc_coro)
# -> coroutine started

print(exc_coro.send(11))
# ->coroutine received: 11
# None

print(exc_coro.send(22))
# ->coroutine received: 22
# None

#닫기
exc_coro.close()
# ->coroutine ending
print(getgeneratorstate(exc_coro)) #GEN_CLOSED #<-종료되었다.