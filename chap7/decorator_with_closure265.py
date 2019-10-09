import time

def clock(func): #<-func가 자유변수가 된다
	''' 함수 호출 시 시간 측정 후 실행 소요시간/전달 인수값/반환값을 출력 '''
	def clocked(*args):
		t0=time.perf_counter()
		result=func(*args)
		elapsed=time.perf_counter()-t0
		name=func.__name__
		arg_str=', '.join(repr(arg) for arg in args)
		print('[%0.8fs] %s(%s) -> %r'%(elapsed,name,arg_str,result))
		return result
	return clocked


@clock
def snooze(seconds):
	time.sleep(seconds)

@clock
def factorial(n):
	return 1 if n<2 else n*factorial(n-1)

if __name__=='__main__':
	print('*'*40,'Calling snooze(.123)')
	snooze(.123)
	print('*'*40,'Calling factorial(6)')
	print('6!=',factorial(6))

	#inspection
	print(factorial.__name__) #clocked #<-데커레이트된 함수의 속성을 가림. factorial=clock(factorial)인 것이 직접 보임
	try:
		factorial(n=6) #TypeError: clocked() got an unexpected keyword argument 'n' #<-keyword 인수로 못넘김. *args로 받기 때문
	except TypeError:
		print('TypeError rise.')



#개선: functools.wraps() 를 이용하여 func에서 clocked로 속성(__name__,__doc__ 등)을 복사.
#개선2: **kwargs도 받자

import functools
def clock2(func):
	''' 함수 호출 시 시간 측정 후 실행 소요시간/전달 인수값/반환값을 출력. clock의 개선 '''
	@functools.wraps(func)
	def clocked(*args,**kwargs):
		t0=time.perf_counter()
		result=func(*args,**kwargs)
		elapsed=time.perf_counter()-t0
		name=func.__name__
		arg_lst=[]
		if args:
			arg_lst.append(', '.join(repr(arg) for arg in args))
		if kwargs:
			pairs=['%s=%r'%(k,w) for k,w in sorted(kwargs.items())]
			arg_lst.append(', '.join(pairs))
		arg_str=', '.join(arg_lst)
		print('[%0.8fs] %s(%s) -> %r'%(elapsed,name,arg_str,result))
		return result
	return clocked

@clock2
def snooze(seconds):
	time.sleep(seconds)

@clock2
def factorial(n):
	return 1 if n<2 else n*factorial(n-1)


if __name__=='__main__':
	print('*'*40,'Calling snooze(.123)')
	snooze(.123)
	print('*'*40,'Calling factorial(6)')
	print('6!=',factorial(n=6)) #<-keyword 인수

	#inspection
	print(factorial.__name__) #factorial #func의 정보가 복사되었다.
	


