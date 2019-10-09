#yield from

#다른 제너레이터에서 생성된 값을 상위 제너레이터 함수가 생성해야 할 때 (즉, 제너레이터 조합 시)
#중첩된 for문을 피할 수 있도록 하는 구문
#코루틴에서도 사용됨

#기존 수작업
def chain(*iterables):
	for it in iterables:
		for i in it:
			yield i

s='ABC'
t=tuple(range(3))
print(list(chain(s,t))) #['A', 'B', 'C', 0, 1, 2]


#yield from 사용 시
def chain2(*iterables):
	for it in iterables:
		yield from it #<-for문을 생략하고 바로 it에서 꺼내온다

print(list(chain2(s,t))) #['A', 'B', 'C', 0, 1, 2]

