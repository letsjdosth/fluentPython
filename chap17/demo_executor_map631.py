from time import sleep, strftime
from concurrent import futures

def display(*args):
	print(strftime('[%H:%M:%S]'), end=' ') #timestamp
	print(*args)

def loiter(n):
	msg='{}loiter({}): doing nothing for {}s...'
	display(msg.format('\t'*n, n, n))
	sleep(n)
	msg='{}loiter({}): done.'
	display(msg.format('\t'*n, n))
	return n*10

def main():
	display('Script starting.')
	executor=futures.ThreadPoolExecutor(max_workers=3)
	results=executor.map(loiter, range(5))
	display('results:',results)
	display('Waiting for individual results:')
	for i, result in enumerate(results):
		display('result {}: {}'.format(i, result))

main()

# [08:17:57] Script starting.
# [08:17:57] loiter(0): doing nothing for 0s...
# [08:17:57] loiter(0): done.
# [08:17:57] 	loiter(1): doing nothing for 1s...
# [08:17:57] 		loiter(2): doing nothing for 2s... #<-스레드가 최대 3개로 설정되었으므로, 일단 3개가 돈다. 0은 0초 sleep이므로 다른 스레드가 시작되기도 전에 곧바로 완료되었다(29줄)(이 양상은 매번 다를 수 있다)
# [08:17:57][08:17:57] 			loiter(3): doing nothing for 3s... #<-이어서 3이 돈다. 이제 스레드 3개가 돌고 있으므로 나머지는 대기한다.
#  results: <generator object Executor.map.<locals>.result_iterator at 0x02ECE2F0> #<-20번째줄의 출력. 제너레이터가 일단 리턴된다.
# [08:17:57] Waiting for individual results:
# [08:17:57] result 0: 0 #<-제너레이터에서 먼저 나온다 (!!)map은 언제나 호출한 순서 그대로 결과를 반환한다.
# [08:17:58] 	loiter(1): done.
# [08:17:58] 				loiter(4): doing nothing for 4s... #<-1이 1초 sleep한 후 끝나고 이어 해당 스레드에서 4가 돈다.
# [08:17:58] result 1: 10 #<-완료되는대로 제너레이터에서 꺼내진다. (!!)for문은 iter(enumerate(results))에서 next를 호출할 때, 해당 객체의 __next__의 블로킹에 대기하다가 블로킹이 해제되면 돈다.
# [08:17:59] 		loiter(2): done.
# [08:17:59] result 2: 20
# [08:18:00] 			loiter(3): done.
# [08:18:00] result 3: 30
# [08:18:02] 				loiter(4): done.
# [08:18:02] result 4: 40

#주의! sleep()은 파이썬의 전역 인터프리터 락(global interpreater lock)을 우회한다.(즉, 재워놓고 다른 스레드가 동작하도록 만들 수도 있다.) 따라서 중간에 스레드 실행순서가 예측불가능하게 바뀔 수 있다.