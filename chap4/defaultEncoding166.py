import sys, locale

expressions="""
	locale.getpreferredencoding()
	type(my_file)
	my_file.encoding
	sys.stdout.isatty()
	sys.stdout.encoding
	sys.stdin.isatty()
	sys.stdin.encoding
	sys.stdin.isatty()
	sys.stdin.encoding
	sys.getdefaultencoding()
	sys.getfilesystemencoding()
"""
my_file=open('dummy','w')
for expression in expressions.split():
	value=eval(expression)
	print(expression.rjust(30),'->',repr(value))

#eval(expression, globals=None, locals=None)
#인자는 문자열 및 선택적 globals 및 locals다. 제공된 경우, globals 는 딕셔너리여야 합니다. 제공되는 경우, locals 는 모든 매핑 객체가 될 수 있습니다.
#expression 인자는 전역 및 지역 이름 공간으로 globals 및 locals 딕셔너리를 사용하여 파이썬 표현식(기술적으로 말하면, 조건 목록)으로 파싱 되고 값이 구해집니다. 
#globals 사전이 제공되고 키 '__builtins__'의 값을 담고 있지 않으면, expression를 구문 분석하기 전에 내장 모듈 builtins의 딕셔너리에 대한 참조를 그 키로 삽입합니다. 
#이는 expression 이 일반적으로 표준 builtins 모듈에 대한 모든 액세스 권한을 가지며 제한된 환경이 전파됨을 뜻합니다. 
#locals 딕셔너리를 생략하면 기본적으로 globals 딕셔너리가 사용됩니다. 두 딕셔너리가 모두 생략되면, 표현식은 eval() 이 호출되는 환경에서 실행됩니다. 
#반환 값은 계산된 표현식의 결과입니다. 


#  locale.getpreferredencoding() -> 'cp949' #윈도우의 선호 인코딩. 가장 중요한 것임
#                  type(my_file) -> <class '_io.TextIOWrapper'>
#               my_file.encoding -> 'cp949' #기본적으로 txt파일은 선호인코딩으로 나감
#            sys.stdout.isatty() -> False  #출력이 콘솔로 나가는지 (이 파이선 파일 실행환경에 따라 달라짐.)
#            sys.stdout.encoding -> 'utf-8' #콘솔에는 utf8로 나감
#             sys.stdin.isatty() -> False
#             sys.stdin.encoding -> 'utf-8'
#             sys.stdin.isatty() -> False
#             sys.stdin.encoding -> 'utf-8'
#       sys.getdefaultencoding() -> 'utf-8' #파일명 인코딩/디코딩시 사용
#    sys.getfilesystemencoding() -> 'utf-8'

#mac이나 linux는 모든 곳에서 utf-8임. 윈도우만 개판