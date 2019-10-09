#context manager 구현 예
#프로토콜: __enter__(self), __exit__(self, exc_type, exc_value, traceback)

class LookingGlass:
	def __enter__(self): #<-self만 인수로 가진다
		import sys
		self.original_write=sys.stdout.write
		sys.stdout.write=self.reverse_write #멍키패칭
		return 'JABBERWOCKY'

	def reverse_write(self,text):
		self.original_write(text[::-1])

	def __exit__(self, exc_type, exc_value, traceback): #<-이 3가지 인수는 with문 빠져나갈 때 파이썬 인터프리터가 제공한다. 정상 수행 시 None,None,None을 인수로 받게 된다.
		import sys
		sys.stdout.write=self.original_write #원래대로 돌려놓는다
		if exc_type is ZeroDivisionError:
			print('Please DO NOT divide by zero!')
			return True #<-예외처리되었음을 파이썬 인터프리터에게 True를 넘겨 알려야 한다.
	#__exit__이 True 이외의 값을 반환하거나 None을 반환하면(즉 아무것도 반환하지 않으면) with 블록에서 발생한 예외가 상위 코드로 전달된다
	
	#__exit__ argument. (참고: 이는 try/finally문의 finally 블록에서 sys.exc_info()를 호출해 받는 정보와 동일하다)
	#exc_type: 예외 클래스
	#exc_value: 예외 객체. 예외 메시지 등은 exc_value.args 속성을 이용해 접근할 수 있다
	#traceback: traceback 객체


#for test
with LookingGlass() as what:
	print('Alice, Kitty and Snowdrop') #pordwonS dna yttiK ,ecilA #<-__enter__에서 sys.stdout.write를 멍키패칭한 대로 나온다
	print(what) #YKCOWREBBAJ #<-__enter__의 리턴이 as 뒤 변수에 들어간다.

print(what) #JABBERWOCKY
print('Back to normal.') #Back to normal.


#with문 없이 사용 시 (what 대신 monster 사용)
manager=LookingGlass()
print(manager) #<__main__.LookingGlass object at 0x00000195DD4ED1D0>
monster=manager.__enter__()
print('Alice, Kitty and Snowdrop')
print(monster) #YKCOWREBBAJ
#print(manager) #>0D1DE4DD59100000x0 ta tcejbo ssalGgnikooL.__niam__<
manager.__exit__(None,None,None)
print(monster) #JABBERWOCKY
print('Back to normal.') #Back to normal.