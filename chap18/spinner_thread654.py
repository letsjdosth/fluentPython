import threading
import itertools
import time
import sys

class Signal:
	go=True

def spin(msg, signal):
	write, flush=sys.stdout.write, sys.stdout.flush
	for char in itertools.cycle('|/-\\'): #<-무한루프이다
		status=char+' '+msg
		write(status)
		flush()
		write('\x08'*len(status))
		time.sleep(.1)
		if not signal.go:
			break
	write(' '*len(status)+'\x08'*len(status))

def slow_function():
	#입출력을 위해 장시간 기다리는 것처럼 보이게 만든다
	time.sleep(3) #sleep은 GIL을 우회하게 만드므로, 그 동안 두번째 스레드가 실행된다.
	return 42

def supervisor():
	signal=Signal()
	spinner=threading.Thread(target=spin,args=('thinking!',signal)) #스레드 생성
	print('spinner object:',spinner)
	spinner.start() #스레드 실행
	result=slow_function() #주 스레드는 slow_function을 실행하고, sleep하게 된다.
	signal.go=False #return 뒤에 주 스레드가 signal을 변경해, 두번째 스레드에 중지 메시지를 보낸다. (파이썬엔 스레드를 중지시키는 API가 정의되어있지 않다. 메시지를 보내야 한다.)
	spinner.join() #2번째 스레드가 완전히 끝날때까지 기다린다.
	return result

def main():
	result=supervisor()
	print('Answer:',result)

if __name__=='__main__':
	main()