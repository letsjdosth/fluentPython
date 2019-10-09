registry=set()

def register(active=True):
	def decorate(func):
		print('running register(active=%s)->decorate(%s)' % (active,func))
		if active:
			registry.add(func)
		else:
			registry.discard(func)
		return func
	return decorate  #<-func가 아니라 decorate를 반환한다! (클로저 이용). register는 일종의 데코레이터 팩토리

@register(active=False) #<-팩토리의 인자를 넘긴다. 그러면 register의 active=False를 자유변수로 가진 decorate(f1())으로 f1이 치환됨
def f1():
	print('running f1()')

@register() #<-마찬가지로 register의 active=True를 자유변수로 가진 decorate(f2())로 치환됨. register를 함수로 (뒤에 ()붙여) 호출해야 한다는 것에 주의!
def f2():
	print('running f2()')

def f3():
	print('running f3()')

print('running main()')
print('registry ->',registry)
f1()
f2()
f3()

'''
출력
running register(active=False)->decorate(<function f1 at 0x000001E72CC40268>) #<-데코레이터 변환은 (매개변수 상관없이 어쨌든) 임포트타임에 실행
running register(active=True)->decorate(<function f2 at 0x000001E72CC402F0>) #<-데코레이터 변환은 임포트타임에 실행
running main()
registry -> {<function f2 at 0x000001E72CC402F0>}  #<-f2만 있다. active arg값에 따라 if문이 돌았기 때문
running f1()
running f2()
running f3()
'''

#일반함수형태로 데코레이터 쓰기
register()(f3) #register(인자)(f) 형태로 불러야 한다. register(인자)=decorate 이므로 (리턴을 잘 보시오!)
print('registry ->',registry)
'''
출력
running register(active=True)->decorate(<function f3 at 0x000001C92FA60158>)
registry -> {<function f3 at 0x000001C92FA60158>, <function f2 at 0x000001C92FA60268>}
'''