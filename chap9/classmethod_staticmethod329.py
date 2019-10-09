class Demo:
	@classmethod
	def klassmeth(*args):
		return args

	@staticmethod
	def statmeth(*args):
		return args

print(Demo.klassmeth()) #(<class '__main__.Demo'>,) #<-첫 인수로 자기 class가 들어가있다.
print(Demo.klassmeth('spam')) #(<class '__main__.Demo'>, 'spam') #<-마찬가지로 스스로가 첫 인수가 된다

print(Demo.statmeth()) #() #<-첫 인수에 자기가 안들어가있다
print(Demo.statmeth('spam')) #('spam',) #<-일반 함수와 전혀 다르지 않다 #(모듈에서 정의하는것과 호출방법 빼고는 전혀 다르지 않다)

