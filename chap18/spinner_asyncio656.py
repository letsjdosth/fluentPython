import asyncio
import itertools
import sys

@asyncio.coroutine
def spin(msg):
	write, flush=sys.stdout.write, sys.stdout.flush
	for char in itertools.cycle('|/-\\'):
		status=char+' '+msg
		write(status)
		flush()
		write('\x08'*len(status))
		try:
			yield from asyncio.sleep(.1)
		except asyncio.CancelledError:
			break
	write(' '*len(status)+'\x08'*len(status))

@asyncio.coroutine
def slow_function():
	yield from asyncio.sleep(3)
	return 42

@asyncio.coroutine
def supervisor():
	spinner=asyncio.ensure_future(spin('thinking!')) #Future, Task, 코루틴, 어웨이터블을 Task 객체를 반환
	# asyncio.async(spin('thinking!')) #책 원본 #<-파이썬 버전 올라오며 삭제된 듯
	print('spinner object:',spinner)
	result=yield from slow_function()
	spinner.cancel() #취소시 중단된 곳의 yield from에서 CancelledError가 발생한다. (spin()에서 이 에러를 이용하고 있다.)
	return result

def main():
	loop=asyncio.get_event_loop()
	result=loop.run_until_complete(supervisor()) # loop.run_until_complete(): 완료할 때까지 퓨처/태스크/어웨이터블을 실행합니다.
	loop.close()
	print('Answer:',result)

if __name__=='__main__':
	main()