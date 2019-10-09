#functools.lru_cache() : memoization. (least recent used)
#이전에 실행한 함수의 결과를 저장하여 같은 인수에 대한 계산을 다시 안 하도록 함

import functools
import time

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
def fibonacci(n):
	if n<2:
		return n
	return fibonacci(n-2)+fibonacci(n-1)

if __name__=='__main__':
	print(fibonacci(6))
'''
#출력
[0.00000032s] fibonacci(0) -> 0
[0.00000032s] fibonacci(1) -> 1
[0.00003529s] fibonacci(2) -> 1
[0.00000000s] fibonacci(1) -> 1
[0.00000032s] fibonacci(0) -> 0
[0.00000032s] fibonacci(1) -> 1
[0.00001508s] fibonacci(2) -> 1
[0.00029514s] fibonacci(3) -> 2
[0.00033973s] fibonacci(4) -> 3
[0.00000000s] fibonacci(1) -> 1
[0.00000032s] fibonacci(0) -> 0
[0.00000000s] fibonacci(1) -> 1
[0.00000770s] fibonacci(2) -> 1
[0.00001732s] fibonacci(3) -> 2
[0.00000000s] fibonacci(0) -> 0
[0.00000032s] fibonacci(1) -> 1
[0.00000770s] fibonacci(2) -> 1
[0.00000032s] fibonacci(1) -> 1
[0.00000000s] fibonacci(0) -> 0
[0.00000032s] fibonacci(1) -> 1
[0.00000770s] fibonacci(2) -> 1
[0.00001476s] fibonacci(3) -> 2
[0.00002951s] fibonacci(4) -> 3
[0.00005422s] fibonacci(5) -> 5
[0.00040196s] fibonacci(6) -> 8

#같은 값을 엄청나게 여러번 계산함
'''
#개선:
print('='*20)
@functools.lru_cache() #<-주의. ()를 붙여야함. 추가 인수를 2개 선택적으로 받기 때문
@clock2
def fibonacci(n):
	if n<2:
		return n
	return fibonacci(n-2)+fibonacci(n-1)

if __name__=='__main__':
	print(fibonacci(6))

'''
#출력
====================
[0.00000032s] fibonacci(0) -> 0
[0.00000064s] fibonacci(1) -> 1
[0.00034903s] fibonacci(2) -> 1
[0.00000096s] fibonacci(3) -> 2
[0.00037470s] fibonacci(4) -> 3
[0.00000032s] fibonacci(5) -> 5
[0.00038400s] fibonacci(6) -> 8
8
'''

#인수: functools.lru_cache(maxsize=128,typed=False)
#maxsize: 얼마나 많은 호출을 저장할 지 정함. 캐시가 다 차면 가장 오래된 결과 버림 (때문에 lru). 왠만하면 2^n으로 설정
#typed: True일때는 인수의 자료형이 다르면 결과를 따로 저장. (1과 1.0 등)
#캐시는 dict임. 따라서 인수가 해시가능해야
