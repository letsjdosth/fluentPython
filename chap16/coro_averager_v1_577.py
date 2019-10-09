from priming_by_decorator577 import coroutine

@coroutine
def averager():
	total=0.0
	count=0
	average=None
	while True:
		term=yield average
		total+=term
		count+=1
		average=total/count

#for test
if __name__=='__main__':
	coro_avg=averager()
	# next(coro_avg) #<-priming #<-알아서 데코레이터가 해줄 것이다..

	from inspect import getgeneratorstate
	print(getgeneratorstate(coro_avg)) #GEN_SUSPENDED #<-yield문에서 대기하는 것을 확인할 수 있다

	print(coro_avg.send(10)) #10.0
	print(coro_avg.send(30)) #20.0
	print(coro_avg.send(5)) #15.0

