'''
#objective: moving (accumulate) average
avg(10) #10.0
avg(11) #10.5
avg(12) #11.0
'''

#1. using class
class Averager():
	def __init__(self):
		self.series=[]
	def __call__(self,new_value):
		self.series.append(new_value)
		total=sum(self.series)
		return total/len(self.series)
avg1=Averager()
print(avg1(10))
print(avg1(11))
print(avg1(12))

#2. using high-order func
def make_averager():
	series=[] #<-averager() 정의 이전에 만들어둔다
	def averager(new_value):
		series.append(new_value)  #<-make_average()의 series를 가져오게 된다. !!: 함수가 비전역 외부 변수를 다루는 경우는 그 함수가 다른 함수에 정의된 경우 뿐임
		total=sum(series)
		return total/len(series)
	return averager #<-return이 averager이기 때문에, 그 위에있는 series는 averager() 정의의 scope를 뛰어넘어 계속 살아남게 된다.
avg2=make_averager()
print(avg2(10))
print(avg2(11))
print(avg2(12))

print(avg2.__code__.co_varnames) #('new_value', 'total')
print(avg2.__code__.co_freevars) #('series',) #<-자유 변수(free variable)이라는 이름으로 따로 취급된다
print(avg2.__closure__) #(<cell at 0x00000243167564F8: list object at 0x0000024316821148>,) #<-freevar는 __closure__에 저장됨
print(avg2.__closure__[0].cell_contents) #[10, 11, 12]

#closure: 함수를 정의할 때 존재하던 자유 변수에 대한 바인딩을 계속 유지하는 함수 (:=본체에서 정의하지 않고 참조하는 비전역 변수를 포함한 확장된 scope의 함수)
#위 예에서 averager는 closure이다
