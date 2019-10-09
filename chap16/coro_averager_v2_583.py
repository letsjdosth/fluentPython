#코루틴에서 값 반환(return)하기
#활성화할때마다 생성하는것 말고 최후에 의미있는 값 하나를 반환하도록 설계하자

from collections import namedtuple

Result=namedtuple('Result','count average')

def averager():
	total=0.0
	count=0
	average=None
	while True:
		term=yield #<-받기만 하자
		if term is None: #참고: None이라고 해서 send()로 비워 보내면 arg가 필요하다고 에러가 뜬다. 명시적으로 None을 넘길 것
			break #코루틴에서 값이 안들어오면 while문을 빠져나가 평균을 반환하도록 한다
		total+=term
		count+=1
		average=total/count
	return Result(count,average) #<-제너레이터가 return을 가지고 있다! (파이썬 3.3 이하에서는 에러난다)

#for test
test=2 #1/2 선택
if test==1: #예외에 밀반입(..)되는 리턴의 모양 보기
	coro_avg=averager()
	next(coro_avg)
	coro_avg.send(10)
	coro_avg.send(30)
	coro_avg.send(6.5)
	coro_avg.send(None) 
	#Traceback (most recent call last):
	# File "C:\newpyscript\fluentPython\chap16\coro_averager_v2_583.py", line 28, in <module>
    # print(coro_avg.send(None))
	#StopIteration: Result(count=3, average=15.5) #<-예외를 뱉으며, 예외 객체의 value 속성으로 리턴한다.

if test==2: #예외처리로 리턴값 뽑기
	coro_avg=averager()
	next(coro_avg)
	coro_avg.send(10)
	coro_avg.send(30)
	coro_avg.send(6.5)
	try:
		coro_avg.send(None)
	except StopIteration as exc:
		result=exc.value
		print(result) #Result(count=3, average=15.5)

#yield from 구문이 StopIteration을 내부적으로 잡아서 자동으로 처리하므로, 이와 엮어 쓰면 편리하다 (뒤 참고)