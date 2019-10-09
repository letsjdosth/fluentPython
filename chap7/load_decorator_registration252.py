registry=[]

def register(func):
	print('running register(%s)'%func)
	registry.append(func)
	return func

@register
def f1():
	print('running f1()')

@register
def f2():
	print('running f2()')

def f3():
	print('running f3()')

def main():
	print('running main()')
	print('registry ->',registry)
	f1()
	f2()
	f3()

if __name__=='__main__':
	main()


'''
*main으로 실행 시 출력:
running register(<function f1 at 0x0000017BDEB40158>)  #!! 처음에(main보다 먼저!) decorator func가 실행된다.
running register(<function f2 at 0x0000017BDEB401E0>)  #!! 두번 걸어서 두번 실행되었다
running main()
registry -> [<function f1 at 0x0000017BDEB40158>, <function f2 at 0x0000017BDEB401E0>]  #!! 데커레이트된(변환된) 함수 참조를 이미 가지고 시작하게 된다
running f1()
running f2()
running f3()

*콘솔에서 임포트시 출력
>>> import load_decorator_registration252
running register(<function f1 at 0x00000244CECC01E0>)  #!! 임포트시 데커레이터 실행! 해당 함수를 변환하여 참조를 가지고있는다.
running register(<function f2 at 0x00000244CECC0268>)  #!! decorator는 import time 실행
>>> load_decorator_registration252.registry
[<function f1 at 0x0000028F19E20158>, <function f2 at 0x0000028F19E20268>]
'''

