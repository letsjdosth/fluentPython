def clip(text, max_len=80):
	"""max_len 앞이나 뒤의 마지막 공백에서 뒤를 잘라낸 텍스트 반환"""
	end=None
	if len(text)>max_len:
		space_before=text.rfind(' ',0,max_len) #rfind(sub,[start,[end]]): reverse find. [start:end]에서, 뒤에서부터 찾음
		if space_before>=0:
			end=space_before
		else:
			space_after=text.rfind('',max_len)
			if space_after>=0:
				end=space_after
	if end is None:
		end=len(text)
	return text[:end].rstrip() 
'''
str.rstrip([chars]) : 후행 문자가 제거된 문자열의 복사본을 돌려줍니다. chars 인자는 제거할 문자 집합을 지정(생략시 공백)
>>> '   spacious   '.rstrip()
'   spacious'
>>> 'mississippi'.rstrip('ipz')
'mississ'
'''

#introspection
print(clip.__defaults__) #(80,) #<-기본값. 단, 인수 순서와 거꾸로 들어가있음
print(clip.__code__) #<code object clip at 0x000001406F472C00, file "C:\newpyscript\fluentPython\chap5\functionIntrospection_clip212.py", line 1>
print(clip.__code__.co_varnames) #('text', 'max_len', 'end', 'space_before', 'space_after') #<-함수본체의 지역변수도 들어있음
print(clip.__code__.co_argcount) #2 #<-여기에는 함수 선언부의 인수 개수만.
#co_varnames 중 앞 co_argcount 개만 함수 인수임
#따라서, text, max_len만 인수이고, defaults tuple (80,)을 거꾸로 보아, text의 기본값은 None, max_len의 기본값은 80임을 알 수 있음


#더 나은 방법: inspect 모듈
from inspect import signature
sig=signature(clip)
print(str(sig)) #(text, max_len=80)
for name, param in sig.parameters.items():
	print(param.kind, ':', name, '=',param.default)
# POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'> #:None
# POSITIONAL_OR_KEYWORD : max_len = 80
'''
#param.kind
POSITIONAL_OR_KEYWORD
VAR_POSITIONAL #*args
VAR_KEYWORD #**kwargs
KEYWORD_ONLY # * 뒤 keyword arg
POSITIONAL_ONLY #python3에서는 사용자 정의 함수의 인수를 이렇게 만들 수 없음. 하지만 C로 구현된 기존 내장함수는 해당사항이 있음
'''

#inspect.signature.bind() #인수를 매개변수에 대응시키는 일반적인 규칙을 적용해서, Signature에 들어있는 매개변수에 바인딩
from functionArguments208 import tag
sig=signature(tag)
my_tag={'name':'img','title':'Sunset Boulevard','src':'sunset.jpg','cls':'framed'}
bound_args=sig.bind(**my_tag)
print(bound_args) #<BoundArguments (name='img', cls='framed', attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>
for name, value in bound_args.arguments.items():
	print(name,'=',value)
# name = img
# cls = framed
# attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}
del my_tag['name']
try:
	bound_args=sig.bind(**my_tag) #TypeError: missing a required argument: 'name'
except TypeError:
	pass
