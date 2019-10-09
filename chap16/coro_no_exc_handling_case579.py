from coro_averager_v1_577 import averager

coro_avg=averager()
print(coro_avg.send(40))
print(coro_avg.send(50))

print(coro_avg.send('spam')) #<-이상한걸 보내보자
# Traceback (most recent call last):
#   File "C:\newpyscript\fluentPython\chap16\coro_no_exc_handling_case579.py", line 7, in <module>
#     print(coro_avg.send('spam'))
#   File "C:\newpyscript\fluentPython\chap16\coro_averager_v1_577.py", line 10, in averager
#     total+=term
#TypeError: unsupported operand type(s) for +=: 'float' and 'str'

#코루틴 안에서 예외가 발생하고, 이것이 호출한 코드 위치로 전파된다
#이후 다시 send()로 호출하면, 곧바로 StopIterration 예외가 발생한다. 즉, 한번 에러나면 해당 제너레이터는 끝이다
#인터프리터에서:
print(coro_avg.send(60))
# Traceback (most recent call last):
#   File "<pyshell#0>", line 1, in <module>
#     print(coro_avg.send(60))
# StopIteration

#이를 이용해 언제나 에러날 값을 보내서 해당 제너레이터를 원할 때 종료시킬수 있다.
#None, Ellipsis(내장 싱클턴 상수 중 하나임)가 많이 쓰임. 그 외에 StopIteration 클래스 자체를 보내버려도 된다.(가독성을 위해)