def make_averager():
	count=0
	total=0
	def averager(new_value):
		nonlocal count,total
		count+=1 #위 nonlocal 선언이 없으면, UnboundLocalError: local variable 'count' referenced before assignment가 남. count=count+1 이어서 count를 재선언/할당하게 되고, 이때 지역변수화 되기 때문
		total+=new_value #total도 마찬가지임
		return total/count
	return averager

#기존 예의 list에서는, append()라는 메소드를 사용해 같은 리스트의 가변 성질을 이용했으므로, 재할당되지 않아서 동작했었음
#nonlocal을 사용할수 없는 경우(python2)에는, 기존 예처럼 list나 dict등 재할당없이 바꿀 수 있는 가변 객체에 넣어 바인딩해야 함
#(int,str,tuple...등등은 불변 객체라 값을 바꾸면 무조건 재할당됨)

avg=make_averager()
print(avg(10))
print(avg(11))
print(avg(12))