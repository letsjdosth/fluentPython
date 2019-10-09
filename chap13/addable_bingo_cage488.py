#가변형의 인플레이스 연산자 구현: 변경 방식

import itertools
from tombola412 import Tombola
from bingo417 import BingoCage

class AddableBingoCage(BingoCage):
	def __add__(self,other):
		if isinstance(other,Tombola): #<-자료형검사를 abc로 하자
			return AddableBingoCage(self.inspect()+other.inspect()) #<-!!!!! 새 객체를 만들어 return한다
		else:
			return NotImplemented

	def __iadd__(self,other):
		if isinstance(other, Tombola):
			other_iterable=other.inspect()
		else:
			try:
				other_iterable=iter(other) #<-어쨌든 순회가능하다면 돌도록 하자. 반복자를 받고 밑에서 load(BingoCage 메소드)한다
			except TypeError:
				self_cls=type(self).__name__
				msg="right operand in += must be {!r} or an iterable"
				raise TypeError(msg.format(self_cls))
		self.load(other_iterable) #<-!!!!! self를 변경하고
		return self #<-!!!!! self를 return한다 (가변형이므로 이렇게 함)


#for test
vowels='AEIOU'
globe=AddableBingoCage(vowels)
print(globe.inspect()) #('A', 'E', 'I', 'O', 'U') #Tombola대로 tuple을 반환한다
assert globe.pick() in vowels
assert len(globe.inspect())==4

#+
globe2=AddableBingoCage('XYZ')
globe3=globe+globe2
assert len(globe3.inspect())==7
try:
	void=globe+[10,20] #<-에러가 나게 한다. +연산자의 경우 리턴 자료형이 어느쪽이어야 하는지가 혼란스럽기 때문
	assert AssertionError
except TypeError:
	pass

#+=
globe_orig=globe
globe+=globe2
assert len(globe.inspect())==7
globe+=['M','N'] #<-에러가 안 나게 한다. +=는 자료형이 AddibleBingoCage가 되는 것이 자연스럽기 때문
assert len(globe.inspect())==9
assert globe is globe_orig #<-같은 객체! +=는 새 객체를 생성하지 않고 기존 객체를 변경했다
try:
	globe+=1
	assert AssertionError
except TypeError:
	pass