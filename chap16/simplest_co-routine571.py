def simple_coroutine():
	print('-> coroutine started')
	x=yield #<-!!!
	print('->coroutne received:',x)

my_coro=simple_coroutine()
print(my_coro) 
#<generator object simple_coroutine at 0x00000196F242B780>

next(my_coro) #<-yield문까지 진행시키자.
#-> coroutine started

my_coro.send(42) #<-yield문까지 도달한 상태에서, 데이터를 보낼 수 있다
#->coroutne received: 42 #<-데이터를 받았다!
#Traceback (most recent call last):
#  File "C:\newpyscript\fluentPython\chap16\simplest_co-routine571.py", line 11, in <module>
#    my_coro.send(42)
#StopIteration #<-일반적인 제너레이터처럼, 끝에 도달하면 StopIteration 예외를 발생시킨다
