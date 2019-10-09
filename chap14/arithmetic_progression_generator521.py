#example
#등차수열 제너레이터

class ArithmeticProgression:
	def __init__(self, begin, step, end=None):
		self.begin=begin
		self.step=step
		self.end=end #none: infinite

	def __iter__(self):
		result=type(self.begin+self.step)(self.begin) #int(object)와 같은 것임. self.begin+self.step의 자료형으로 self.begin을 형변환한다
		forever=self.end is None
		index=0
		while forever or result<self.end:
			yield result
			index +=1
			result=self.begin+self.step*index

#for test #ArithmeticProgression(begin, step[, end])
ap=ArithmeticProgression(0,1,3)
assert list(ap)==[0,1,2]
ap=ArithmeticProgression(1,.5,3)
assert list(ap)==[1.0, 1.5, 2.0, 2.5]
ap=ArithmeticProgression(0,1/3,1)
assert list(ap)==[0,1/3,2/3]
from fractions import Fraction
ap=ArithmeticProgression(0,Fraction(1,3),1)
assert list(ap)==[Fraction(0,1),Fraction(1,3),Fraction(2,3)]
from decimal import Decimal
ap=ArithmeticProgression(0,Decimal('.1'),.3)
assert list(ap)==[Decimal('0.0'),Decimal('0.1'),Decimal('0.2')]


#그런데 위와 같은 일 하려면 그냥 제너레이터 함수 하나 만들면 됨
def aritprog_gen(begin, step, end=None):
	result=type(begin+step)(begin)
	forever=end is None
	index=0
	while forever or result<end:
		yield result
		index +=1
		result=begin+step*index

#for test
ap=aritprog_gen(0,1,3) #(제너레이터 함수는 자체를 호출시에는 초기상태 반복자를 반환한다)
print(next(ap)) #0
print(next(ap)) #1
print(next(ap)) #2
ap=aritprog_gen(0,1,3)
print(list(ap)) #[0, 1, 2]


#itertools 모듈의 제너레이터 이용
import itertools
gen=itertools.count(1,0.5) #itertools.count(begin, step) #<-기본적으로 무한히 만들어낸다
print(next(gen)) #1
print(next(gen)) #1.5
print(next(gen)) #2.0

gen=itertools.takewhile(lambda n:n<3, itertools.count(1,0.5)) #itertools.takewhile(predicate, generator) #제너레이터를 소비하면서, predicate가 False가 되면 중단한다
print(list(gen)) #[1, 1.5, 2.0, 2.5]

def aritprog_gen_2(begin, step, end=None):
	first=type(begin+step)(begin)
	ap_gen=itertools.count(first,step)
	if end is not None:
		ap_gen=itertools.takewhile(lambda n:n<end, ap_gen)
	return ap_gen
	#yield가 없어서 제너레이터 함수는 아니지만, 리턴이 제너레이터이므로, 일종의 제너레이터 팩토리로 기능한다

#for test
ap=aritprog_gen_2(0,1,3)
print(list(ap))