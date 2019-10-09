def averager():
	total=0.0
	count=0
	average=None
	while True: #<-코루틴에서 무한루프를 돌리면 이 제너레이터는 호출자가 .close()를 호출하거나 이 객체에 대한 참조가 모두 없어질때까지(<-파이썬 가비지컬렉터가 잡을 조건) 메모리에 존재하게 된다.
		term=yield average
		total+=term
		count+=1
		average=total/count

#for test
if __name__=='__main__':
	coro_avg=averager()
	next(coro_avg) #<-priming
	print(coro_avg.send(10)) #10.0
	print(coro_avg.send(30)) #20.0
	print(coro_avg.send(5)) #15.0

