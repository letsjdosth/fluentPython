from random import randrange

from tombola412 import Tombola

@Tombola.register #<-아래 클래스를 가상 서브클래스로 등록하자
class TomboList(list): #<-Tombola를 상속받지 않는다. runtime error를 방지하려면 알아서 맞춰서 구현해야 함
					#(이런식으로 상속이 아니라 '등록'한 클래스는 객체 생성시에도 규격을 검사하지 않는다). 런타임시 꼬이는 경우 그때가서 에러를 뱉는다
	def pick(self):
		if self: #==if bool(self)==True : list에서 __bool__을 상속한다. bool(list)는 list가 비어있으면 False, 아니면 True를 반환한다.
			position=randrange(len(self))
			return self.pop(position)
		else:
			raise LookupError('pop from empty TomboList')

	load=list.extend #list의 메소드를 그대로 할당하자

	def loaded(self):
		return bool(self)

	def inspect(self):
		return tuple(sorted(self))


if __name__=='__main__':
	print(issubclass(TomboList,Tombola)) #True
	t=TomboList(range(100))
	print(isinstance(t,Tombola)) #True
	print(TomboList.__mro__) 
	#(<class '__main__.TomboList'>, <class 'list'>, <class 'object'>) 
	#메서드 결정순서에 가상 슈퍼클래스인 Tombola는 없다!! 진짜로 상속된 클래스만 있음