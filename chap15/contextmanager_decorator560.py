# @contextmanager
# https://docs.python.org/ko/3.7/library/contextlib.html?highlight=utility#contextlib.contextmanager
# This function is a decorator that can be used to define a factory function for with statement context managers, 
# without needing to create a class or separate __enter__() and __exit__() methods.

# At the point where the generator yields, the block nested in the with statement is executed. 
# The generator is then resumed after the block is exited. 

# If an unhandled exception occurs in the block, it is reraised inside the generator at the point where the yield occurred. 
# Thus, you can use a try...except...finally statement to trap the error (if any), or ensure that some cleanup takes place. 
# If an exception is trapped merely in order to log it or to perform some action (rather than to suppress it entirely), the generator must reraise that exception. 
# Otherwise the generator context manager will indicate to the with statement that the exception has been handled, and execution will resume with the statement immediately following the with statement.

import contextlib

@contextlib.contextmanager
def looking_glass():
	import sys
	original_write=sys.stdout.write

	def reverse_write(text):
		original_write(text[::-1])

	sys.stdout.write=reverse_write
	msg=''
	try:
		yield 'JABBERWOCKY' #<-@contextmanager를 이용하는 함수는 제너레이터 함수로, 1개의 yield문만 가지고 있어야 한다. 
	#with문 진입 시, yield문까지 실행되고 (__enter__역할). 이후 이 함수는 멈춘다. (내부적으로는 contextmanger 데커레이터가 인수로 받은 함수를 가지고 next()를 한번 실행하는 것임)
	#이후, with문을 나갈 시, yield 다음줄부터 실행된다.(__exit__역할) (내부적으로는 contextmanger 데커레이터가 인수로 받은 함수를 가지고 다시한번 next()를 실행하는 것임)
	#with문에서 예외가 발생했다면, 인터프리터가 일단 with문의 예외를 잡아놓은 후, yield문 위치로 전달해 여기에서 예외를 재발생시킨다. 이를 이용해 예외처리를 할 수 있다.
	except ZeroDivisionError:
		msg='Please DO NOT divide by zero' 
		#__exit__과 달리 @contextmanager는 기본적으로 예외처리를 했다고 가정하고 예외를 상위 코드로 전파하지 않는다.(초기 파이썬의 제너레이터 함수는 값을 생성만 하지 반환할 수 없었기 때문)
		#만약 전파가 필요하다면, 이 함수 내에서 명시적으로 예외를 재발생(raise 이용)시켜야 한다.
		#때문에 일반적으로 try-except-(else)-finally문을 이용해 무조건 예외를 잡는다.(아니면 예외가 나든 말든 걍 씹히고 파이썬 프로그램은 조용히 안멀쩡한 상태로 돌아간다)
	finally:
		sys.stdout.write=original_write
		if msg:
			print(msg)

#for test
with looking_glass() as what:
	print('Alice, Kitty and Snowdrop') #pordwonS dna yttiK ,ecilA #<-__enter__에서 sys.stdout.write를 멍키패칭한 대로 나온다
	print(what) #YKCOWREBBAJ #<-__enter__의 리턴이 as 뒤 변수에 들어간다.

print(what) #JABBERWOCKY
print('Back to normal.') #Back to normal.