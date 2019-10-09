#functools.singledispatch() : Transform a function into a single-dispatch generic function.
#https://docs.python.org/ko/3/library/functools.html#functools.singledispatch
#같은 이름 함수를 인수의 자료형에 따라 다른 함수에 넘겨 처리할 수 있음 (자바 오버로딩처럼..)
#(기존 파이썬 방식으로 하면, if-elif문을 이용해 각 함수로 넘겨주는 디스패치 함수가 필요)
#참고: generic function == 범용 함수 로 번역

from functools import singledispatch
from collections import abc
import numbers

import html

@singledispatch  #기반함수
def htmlize(obj):
	content=html.escape(repr(obj))
	return '<pre>{}</pre>'.format(content)

@htmlize.register(str)  #<기반함수>.register(객체형) 으로 데코레이트 (아니면 함수 arg에 자료형 어노테이션을 달면 그걸로 적용해 가져옴)
def _(text):
	content=html.escape(text).replace('\n','<br>\n')
	return '<p>{}</p>'.format(content)

@htmlize.register(numbers.Integral) #참고: numbers.Integral : int의 가상 슈퍼클래스
def _(n):
	return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence) #<-여러 자료형을 지원하기 위해 데코레이터로 여러개 쌓을 수 있다
def _(seq):
	inner='</li>\n<li>'.join(htmlize(item) for item in seq)
	return '<ul>\n<li>'+inner+'</li>\n</ul>'

#want: 
#str: 개행문자를 <br>\n 으로 대체하고 pre 대신 p 태그를 사용
#int: 숫자를 10진수와 16진수로 동시에 보여줌
#list: 각 항목을 자료형에 따라 포맷한 html 리스트를 출력

#for test
assert htmlize({1,2,3})=='<pre>{1, 2, 3}</pre>'
assert htmlize(abs)=='<pre>&lt;built-in function abs&gt;</pre>'
assert htmlize('Heimlich & Co.\n- a game')=='<p>Heimlich &amp; Co.<br>\n- a game</p>'
assert htmlize(42)=='<pre>42 (0x2a)</pre>'
assert htmlize(['alpha',66,{3,2,1}])=='''<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>'''

